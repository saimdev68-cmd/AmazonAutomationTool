from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView 
from .models import Product , Campaign
from django.db.models import Sum , F
import pandas as pd
from django.http import JsonResponse
from django.views import View
from .forms import CampaignForm
from django.shortcuts import render , get_object_or_404 , redirect

# Create your views here.

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "demo_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = self.request.user.seller
        products = Product.objects.filter(seller=seller)
        product_summary = products.aggregate(
            gross_sales = Sum("gross_revenue"),
            amazon_fees = Sum("total_fees"),
            ppc_spend = Sum("ad_spend"),
            net_profit = Sum("net_profit"),
        )
        gross_sales = int(product_summary["gross_sales"]) or 0
        amazon_fees = int(product_summary["amazon_fees"]) or 0
        ppc_spend = int(product_summary["ppc_spend"]) or 0
        net_profit = int(product_summary["net_profit"]) or 0
        avg_daily_profit = int(net_profit / 30) if net_profit else 0
        tacos = round((ppc_spend / gross_sales) * 100,1) if gross_sales else 0
        context.update({
            "seller":seller,
            "products":products,
            "gross_sales": gross_sales,
            "amazon_fees": amazon_fees,
            "ppc_spend": ppc_spend,
            "net_profit": net_profit,
            "avg_daily_profit": avg_daily_profit,
            "tacos":tacos

        })
        return context
    
class DemoDashboardView(LoginRequiredMixin,TemplateView):
    template_name = "demo_dashboard.html"


    
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
        
class FinanceView(LoginRequiredMixin, TemplateView):
    template_name = "demo_finance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(seller=self.request.user.seller)
        product_summary = products.aggregate(
            total_revenue = Sum("gross_revenue"),
            cogs = Sum("cogs"),
            ad_spend = Sum("ad_spend"),
            margin = Sum("margin"),
            fba_fees = Sum(F('fba_fee') + F('storage_fee') +F('advertising_fee')),
            referral_fee = Sum("amazon_referral_fee")
        )
        total_products = products.count()
        total_revenue = int(product_summary["total_revenue"]) or 0
        margin = round(product_summary["margin"] / total_products,1) if total_products else 0
        ad_spend = int(product_summary["ad_spend"]) or 0
        tacos = round((ad_spend / total_revenue) * 100,1) if total_revenue else 0
        cogs = int(product_summary["cogs"]) or 0
        cogs_per = round((cogs / total_revenue) * 100,1) if total_revenue else 0
        fba_fees = int(product_summary["fba_fees"]) or 0
        fba_fees_per = round((fba_fees/ total_revenue) * 100,1) if total_revenue else 0
        referral_fee = int(product_summary["referral_fee"]) or 0
        referral_fee_per = round((referral_fee/ total_revenue) * 100,1) if total_revenue else 0
        gross_profit = total_revenue - cogs - fba_fees - referral_fee
        gross_profit_per = round((gross_profit / total_revenue) * 100,1) if total_revenue else 0
        net_profit = gross_profit - ad_spend
        net_profit_per = round((net_profit / total_revenue) * 100,1) if total_revenue else 0
        context.update({
            "products":products,
            "total_revenue":total_revenue,
            "net_profit":net_profit,
            "margin":margin,
            "tocas":tacos,
            "cogs":cogs,
            "cogs_per":cogs_per,
            "fba_fees":fba_fees,
            "fba_fees_per":fba_fees_per,
            "referral_fee":referral_fee,
            "referral_fee_per":referral_fee_per,
            "ad_spend":ad_spend,
            "gross_profit":gross_profit,
            "gross_profit_per":gross_profit_per,
            "net_profit_per":net_profit_per
        })
        return context
    

class DemoFinanceView(LoginRequiredMixin, TemplateView):
    template_name = "demo_finance.html"

import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def export_financial_report_csv(request):
    # 1. Setup the HTTP response with CSV headers
    response = HttpResponse(content_type='text/csv')
    filename = f"profitlens_report_{datetime.now().strftime('%Y%m%d')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)

    # 2. Write Document Metadata Meta-Rows
    writer.writerow(["ProfitLens Financial Report", f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"])
    writer.writerow([]) # Empty spacer row

    # 3. Section 1: Profit & Loss Statement Summary Rows
    writer.writerow(["--- PROFIT & LOSS SUMMARY ---"])
    writer.writerow(["Metric", "Amount ($)", "Percentage (%)"])
    
    pl_data = [
        ["Revenue", 95320, "100.0%"],
        ["COGS", -28932, "-30.4%"],
        ["FBA Fees", -9532, "-10.0%"],
        ["Referral Fees", -14300, "-15.0%"],
        ["Gross Profit", 42556, "44.6%"],
        ["PPC / Ad Spend", -22113, "-23.2%"],
        ["Net Profit", 20443, "21.4%"],
    ]
    for row in pl_data:
        writer.writerow(row)

    writer.writerow([]) # Empty spacer row
    writer.writerow([]) # Empty spacer row

    # 4. Section 2: Detailed SKU Performance Rows
    writer.writerow(["--- SKU-LEVEL BREAKDOWN ---"])
    writer.writerow(["Product", "Revenue ($)", "COGS ($)", "Fees ($)", "Gross Profit ($)", "Ad Spend ($)", "Net Profit ($)", "Margin (%)"])
    
    sku_data = [
        ["Premium Yoga Mat - Black", 10260, 3420, 2566, 4274, 2052, 2222, "21.7%"],
        ["Stainless Steel Water Bottle 32oz", 15540, 4662, 3885, 6993, 3108, 3885, "25.0%"],
        ["Organic Green Tea - 100 Bags", 17820, 4455, 4455, 8910, 3564, 5346, "30.0%"],
        ["LED Desk Lamp - Adjustable", 8350, 3340, 2088, 2922, 2505, 417, "5.0%"],
        ["Bamboo Cutting Board Set", 8520, 2840, 2130, 3550, 1704, 1846, "21.7%"],
        ["Silicone Kitchen Utensil Set", 12690, 3807, 3173, 5710, 2538, 3172, "25.0%"],
        ["Resistance Bands Set - 5 Pack", 12240, 2448, 3060, 6732, 3672, 3060, "25.0%"],
        ["Aromatherapy Diffuser - Wood Grain", 9900, 3960, 2475, 3465, 2970, 495, "5.0%"],
    ]
    for row in sku_data:
        writer.writerow(row)

    return response

class DemoCompaignView(LoginRequiredMixin,TemplateView):
    template_name = "demo_compaign.html"