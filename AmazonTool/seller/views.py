from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView 
from .models import Product , Campaign , OrderItem , Order
import pandas as pd
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404 , redirect
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime , timedelta
from django.db.models import F, Sum, DecimalField, ExpressionWrapper , Value , Q
from django.utils import timezone
from django.db.models.functions import Coalesce , TruncDate
import json
from decimal import Decimal
from support.utils import create_audit_log
from support.models import AuditLog

# Create your views here.

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = self.request.user.seller
        last_30_days = timezone.now().date() - timedelta(days=30)

        items = OrderItem.objects.filter(
            seller=seller,
            order__purchase_date__gte=last_30_days,
        )

        gross_revenue = items.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("price") * F("quantity"),
                    output_field=DecimalField(max_digits=14, decimal_places=2),
                )
            )
        )["total"] or 0

        amazon_fees = items.aggregate(
            total=Sum("fees")
        )["total"] or 0

        net_profit = items.aggregate(
            total=Sum(
                ExpressionWrapper(
                    (F("price") - F("cost")) * F("quantity") - F("fees"),
                    output_field=DecimalField(max_digits=14, decimal_places=2),
                )
            )
        )["total"] or 0

        ppc_spend = items.aggregate(
            total=Sum("ads_cost")
        )["total"] or Decimal("0.00")

        # TACoS = PPC Spend / Total Revenue * 100
        tacos_per = (
            (ppc_spend / gross_revenue) * Decimal("100")
            if gross_revenue > 0
            else Decimal("0.00")
        )

        products = (
            Product.objects.filter(seller=seller)
            .annotate(
                quantity_sold=Coalesce(
                    Sum(
                        "orderitem__quantity",
                        filter=Q(orderitem__order__purchase_date__gte=last_30_days),
                    ),
                    Value(0),
                ),
                revenue=Coalesce(
                    Sum(
                        ExpressionWrapper(
                            F("orderitem__price") * F("orderitem__quantity"),
                            output_field=DecimalField(max_digits=14, decimal_places=2),
                        ),
                        filter=Q(orderitem__order__purchase_date__gte=last_30_days),
                    ),
                    Value(0),
                    output_field=DecimalField()
                ),
                net_profit=Coalesce(
                    Sum(
                        ExpressionWrapper(
                            (F("orderitem__price") - F("orderitem__cost"))
                            * F("orderitem__quantity")
                            - F("orderitem__fees"),
                            output_field=DecimalField(max_digits=14, decimal_places=2),
                        ),
                        filter=Q(orderitem__order__purchase_date__gte=last_30_days),
                    ),
                    Value(0),
                    output_field=DecimalField()
                ),
            )
        )

        for product in products:
            if product.revenue:
                product.margin = round((product.net_profit / product.revenue) * 100, 2)
            else:
                product.margin = 0

        daily_stats = (
            OrderItem.objects.filter(
                seller=seller,
                order__purchase_date__gte=last_30_days,
            )
            .annotate(day=TruncDate("order__purchase_date"))
            .values("day")
            .annotate(
                revenue=Sum(
                    ExpressionWrapper(
                        F("price") * F("quantity"),
                        output_field=DecimalField(max_digits=14, decimal_places=2),
                    )
                ),
                net_profit=Sum(
                    ExpressionWrapper(
                        (F("price") - F("cost")) * F("quantity") - F("fees"),
                        output_field=DecimalField(max_digits=14, decimal_places=2),
                    )
                ),
                ppc_spend=Sum("ads_cost"),
            )
        )

        # Convert queryset into a dictionary
        stats = {
            row["day"]: row
            for row in daily_stats
        }

        labels = []
        revenues = []
        profits = []
        tacos = []

        current = last_30_days
        today = timezone.now().date()

        while current <= today:
            row = stats.get(current)

            if row:
                revenue = float(row["revenue"] or 0)
                profit = float(row["net_profit"] or 0)
                ppc = float(row["ppc_spend"] or 0)

                taco = (ppc / revenue * 100) if revenue > 0 else 0
            else:
                revenue = 0
                profit = 0
                taco = 0

            labels.append(current.strftime("%d %b"))
            revenues.append(revenue)
            profits.append(profit)
            tacos.append(round(taco, 2))

            current += timedelta(days=1)

        context["chart_labels"] = json.dumps(labels)
        context["chart_revenue"] = json.dumps(revenues)
        context["chart_profit"] = json.dumps(profits)
        context["chart_tacos"] = json.dumps(tacos)

        context["products"] = products
        context["avg_daily_profit"] = round(net_profit / 30)
        context["revenue_30_days"] = gross_revenue
        context["amazon_fees_30_days"] = amazon_fees
        context["net_profit_30_days"] = net_profit
        context["ppc_spend_30_days"] = ppc_spend
        context["tacos_30_days"] = round(tacos_per, 2)
        context["seller"] = seller
        return context
    
class UploadCOGSView(LoginRequiredMixin, View):

    SKU_COLUMNS = ["sku","seller sku","merchant sku","product sku","seller_sku","merchant_sku","asin sku",]
    COST_COLUMNS = ["cogs","cost","unit cost","product cost","product_cost","unit_cost","landed cost",]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse(
                {"success": False, "message": "No file uploaded"},
                status=400,
            )

        try:
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.name.endswith((".xlsx", ".xls")):
                df = pd.read_excel(file)
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Only CSV and Excel files are allowed",
                    },
                    status=400,
                )
            columns = {
                str(col).strip().lower(): col
                for col in df.columns
            }

            sku_column = None
            for col in self.SKU_COLUMNS:
                if col in columns:
                    sku_column = columns[col]
                    break
            cost_column = None
            for col in self.COST_COLUMNS:
                if col in columns:
                    cost_column = columns[col]
                    break
            if not sku_column:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "SKU column not found",
                    },
                    status=400,
                )

            if not cost_column:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "COGS/Cost column not found",
                    },
                    status=400,
                )
            seller = request.user.seller
            updated = 0
            skipped = 0
            for _, row in df.iterrows():
                sku = str(row[sku_column]).strip()
                if not sku:
                    skipped += 1
                    continue
                try:
                    cost = float(row[cost_column])
                except:
                    skipped += 1
                    continue
                product = Product.objects.filter(
                    seller=seller,
                    sku=sku,
                ).first()
                if product:
                    product.cost = cost
                    product.save(update_fields=["cost"])
                    updated += 1
                else:
                    skipped += 1
            create_audit_log(
                request.user,
                AuditLog.Category.DATA_IMPORT,
                AuditLog.Action.CSV_UPLOAD,
                detail=f"Uploaded COGS CSV {updated} products updated",
            )
            return JsonResponse(
                {
                    "success": True,
                    "updated": updated,
                    "skipped": skipped,
                    "message": f"{updated} products updated",
                }
            )

        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": str(e),
                },
                status=500,
            )
        
class FinanceView(LoginRequiredMixin, TemplateView):
    template_name = "finance.html"

    def get(self, request, *args, **kwargs):

        filter_type = request.GET.get("type")
        period = request.GET.get("period")

        if not filter_type or not period:
            today = timezone.localdate()

            filter_type = "monthly"
            period = today.strftime("%Y-%m")

            return redirect(
                f"{request.path}?type={filter_type}&period={period}"
            )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = self.request.user.seller
        today = timezone.localdate()
        filter_type = self.request.GET.get("type", "monthly")
        period = self.request.GET.get("period")
        months = []
        weeks = []
        current = today.replace(day=1)
        for _ in range(12):
            months.append({"text": current.strftime("%B %Y"),"value": current.strftime("%Y-%m")})
            if current.month == 1:
                current = current.replace(year=current.year - 1,month=12)
            else:
                current = current.replace(month=current.month - 1)
        current = today
        for _ in range(20):
            iso = current.isocalendar()
            weeks.append({"text": f"Week {iso.week} ({iso.year})","value": f"{iso.year}-{iso.week}"})
            current -= timedelta(days=7)
        if not period:
            if filter_type == "monthly":
                period = today.strftime("%Y-%m")
            else:
                iso = today.isocalendar()
                period = f"{iso.year}-{iso.week:02d}"
        revenue_expression = ExpressionWrapper(
            F("price") * F("quantity"),
            output_field=DecimalField(
                max_digits=14,
                decimal_places=2
            )
        )

        cost_expression = ExpressionWrapper(
            F("cost") * F("quantity"),
            output_field=DecimalField(
                max_digits=14,
                decimal_places=2
            )
        )
        qs = OrderItem.objects.filter(seller=seller)
        if filter_type == "monthly":

            year, month = period.split("-")

            qs = qs.filter(
                order__purchase_date__year=year,
                order__purchase_date__month=month
            )

        else:

            year, week = period.split("-")

            qs = qs.filter(
                order__purchase_date__iso_year=year,
                order__purchase_date__week=week
            )
        summary = qs.aggregate(

            revenue=Sum(F("price") *F("quantity")),

            cogs=Sum(F("cost") * F("quantity")),

            referral=Sum("fees"),

            fba=Sum("fba_fees"),

            ads=Sum("ads_cost")

        )

        revenue = summary["revenue"] or Decimal("0")

        cogs = summary["cogs"] or Decimal("0")

        referral = summary["referral"] or Decimal("0")

        fba = summary["fba"] or Decimal("0")

        ads = summary["ads"] or Decimal("0")

        gross_profit = revenue - cogs - referral - fba

        net_profit = gross_profit - ads

        margin = Decimal("0")

        tacos = Decimal("0")

        if revenue:

            margin = (net_profit / revenue) * 100

            tacos = (ads / revenue) * 100

        chart = (
            qs.annotate(
                day=TruncDate(
                    "order__purchase_date"
                )
            )
            .values("day")
            .annotate(

                revenue=Sum(F("price") *F("quantity")),

                cogs=Sum(F("cost") * F("quantity")),

                referral=Sum("fees"),

                fba=Sum("fba_fees"),

                ads=Sum("ads_cost")

            )
            .order_by("day")
        )

        labels = []

        revenue_data = []

        gross_data = []

        net_data = []

        for row in chart:

            revenue = row["revenue"] or Decimal("0")

            gross = (
                revenue
                - (row["cogs"] or Decimal("0"))
                - (row["referral"] or Decimal("0"))
                - (row["fba"] or Decimal("0"))
            )

            net = gross - (row["ads"] or Decimal("0"))

            labels.append(
                row["day"].strftime("%m-%d")
            )

            revenue_data.append(float(revenue))

            gross_data.append(float(gross))

            net_data.append(float(net))

        sku_rows = (

            qs.values(

                "product__sku",

                "product__title"

            )

            .annotate(

                revenue=Sum(F("price") *F("quantity")),

                cogs=Sum(F("cost") * F("quantity")),

                referral=Sum("fees"),

                fba=Sum("fba_fees"),

                ads=Sum("ads_cost")

            )

            .order_by("-revenue")

        )

        sku_table = []

        for row in sku_rows:

            revenue = row["revenue"] or Decimal("0")

            gross = (

                revenue

                - (row["cogs"] or Decimal("0"))

                - (row["referral"] or Decimal("0"))

                - (row["fba"] or Decimal("0"))

            )

            net = gross - (row["ads"] or Decimal("0"))

            margin = Decimal("0")

            if revenue:

                margin = (net / revenue) * 100

            sku_table.append({

                "sku": row["product__sku"],

                "title": row["product__title"],

                "revenue": revenue,

                "cogs": row["cogs"],

                "fees": (row["referral"] or Decimal("0")) + (row["fba"] or Decimal("0")),

                "gross": gross,

                "ads": row["ads"],

                "net": net,

                "margin": round(margin, 2)

            })
        context["months_json"] = json.dumps(months)
        context["months"] = months
        context["weeks_json"] = json.dumps(weeks)
        context["weeks"] = weeks
        context["filter_type"] = filter_type

        context["selected_period"] = period

        context["summary"] = {

            "revenue": revenue,

            "cogs": cogs,

            "referral": referral,

            "fba": fba,

            "ads": ads,

            "gross": gross_profit,

            "net": net_profit,

            "margin": round(margin, 2),

            "tacos": round(tacos, 2)

        }

        context["chart"] = json.dumps({

            "labels": labels,

            "revenue": revenue_data,

            "gross": gross_data,

            "net": net_data

        })

        context["sku_table"] = sku_table

        return context
    
@login_required
def export_financial_report_csv(request):

    seller = request.user.seller
    response = HttpResponse(content_type="text/csv")

    writer = csv.writer(response)

    filter_type = request.GET.get("type", "monthly")
    period = request.GET.get("period")

    qs = OrderItem.objects.filter(seller=seller)

    if filter_type == "monthly":
        year, month = period.split("-")

        qs = qs.filter(
            order__purchase_date__year=year,
            order__purchase_date__month=month,
        )
    else:
        year, week = period.split("-")

        qs = qs.filter(
            order__purchase_date__iso_year=year,
            order__purchase_date__week=week,
        )
    summary = qs.aggregate(

        revenue=Sum(F("price") * F("quantity")),

        cogs=Sum(F("cost") * F("quantity")),

        referral=Sum("fees"),

        fba=Sum("fba_fees"),

        ads=Sum("ads_cost"),

    )
    revenue = summary["revenue"] or Decimal("0")
    cogs = summary["cogs"] or Decimal("0")
    referral = summary["referral"] or Decimal("0")
    fba = summary["fba"] or Decimal("0")
    ads = summary["ads"] or Decimal("0")

    gross = revenue - cogs - referral - fba
    net = gross - ads

    margin = Decimal("0")

    if revenue:
        margin = (net / revenue) * 100

    writer.writerow(["Metric", "Amount", "%"])

    writer.writerow(["Revenue", revenue, "100.00%"])

    writer.writerow([
        "COGS",
        cogs,
        f"{(cogs / revenue * 100):.2f}%" if revenue else "0%"
    ])

    writer.writerow([
        "FBA Fees",
        fba,
        f"{(fba / revenue * 100):.2f}%" if revenue else "0%"
    ])

    writer.writerow([
        "Referral Fees",
        referral,
        f"{(referral / revenue * 100):.2f}%" if revenue else "0%"
    ])

    writer.writerow([
        "Gross Profit",
        gross,
        f"{(gross / revenue * 100):.2f}%" if revenue else "0%"
    ])

    writer.writerow([
        "PPC Spend",
        ads,
        f"{(ads / revenue * 100):.2f}%" if revenue else "0%"
    ])

    writer.writerow([
        "Net Profit",
        net,
        f"{margin:.2f}%"
    ])
    sku_rows = (
        qs.values(
            "product__sku",
            "product__title",
        )
        .annotate(
            revenue=Sum(F("price") * F("quantity")),
            cogs=Sum(F("cost") * F("quantity")),
            referral=Sum("fees"),
            fba=Sum("fba_fees"),
            ads=Sum("ads_cost"),
        )
        .order_by("-revenue")
    )
    for row in sku_rows:

        revenue = row["revenue"] or Decimal("0")

        gross = (
            revenue
            - (row["cogs"] or Decimal("0"))
            - (row["referral"] or Decimal("0"))
            - (row["fba"] or Decimal("0"))
        )

        net = gross - (row["ads"] or Decimal("0"))

        margin = (net / revenue * 100) if revenue else Decimal("0")

        writer.writerow([
            row["product__title"],
            revenue,
            row["cogs"] or 0,
            (row["referral"] or 0) + (row["fba"] or 0),
            gross,
            row["ads"] or 0,
            net,
            f"{margin:.2f}%"
        ])
    create_audit_log(
        request.user,
        AuditLog.Category.REPORT,
        AuditLog.Action.REPORT_DOWNLOAD,
        detail=f"Downloaded {filter_type} Finance Statement {period}",
    )
    return response
    
        
class PPCManagerView(LoginRequiredMixin,TemplateView):

    template_name = "ppc_manager.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compaigns = Campaign.objects.filter(seller=self.request.user.seller)
        context.update({
            "compaigns":compaigns
        })
        return context
    
class PreCreateCompaignView(LoginRequiredMixin,TemplateView):
    template_name = "pre_compaign.html"


class CreateCompaignView(LoginRequiredMixin,TemplateView):
    template_name= "create_compaign.html"

    
class CompaignActionView(LoginRequiredMixin,View):
    def post(self,request,pk):
        compaign = get_object_or_404(Campaign,seller=request.user.seller,pk=pk)
        if compaign.status == Campaign.Status.ACTIVE:
            Campaign.status = Campaign.Status.PAUSED
            compaign.save()
            return redirect ("/")
        else:
            Campaign.status = Campaign.Status.ACTIVE
            compaign.save()
            return redirect ("/")
        

class BrandCompaignView(LoginRequiredMixin,TemplateView):
    template_name = "brand_compaign.html"

class DisplayCompaignView(LoginRequiredMixin,TemplateView):
    template_name = "display_compaign.html"