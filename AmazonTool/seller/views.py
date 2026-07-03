from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Product , Campaign
from django.db.models import Sum 
import pandas as pd
from django.http import JsonResponse
from django.views import View
from .forms import CampaignForm
from django.shortcuts import render , get_object_or_404 , redirect


# Create your views here.

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
            "form":CampaignForm(),
            "compaigns":compaigns
        })
        return context

class CampaignView(LoginRequiredMixin, View):

    def get(self, request):
        form = CampaignForm()
        return render(request, "ppc.html", {"form": form})
    
    def post(self, request):
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            seller = request.user.seller
            campaign.seller = seller
            campaign.save()
            return JsonResponse({
                "success": True, 
                "message": "Campaign created successfully!"
            }, status=200)
            
        return JsonResponse({
            "success": False, 
            "errors": form.errors
        }, status=400)
    
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