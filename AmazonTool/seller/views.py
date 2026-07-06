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

class HomeView(TemplateView):
    template_name = "home.html"

    

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"

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
    template_name = "finance.html"

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
    