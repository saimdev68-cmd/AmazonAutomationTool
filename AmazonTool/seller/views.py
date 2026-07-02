from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
import json
from .models import Product

# Create your views here.

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = self.request.user.seller
        with open("seller/data/products.json") as f:
            product_data = json.load(f)
        products = Product.objects.filter(seller=seller).select_related("seller")
        existing_asins = set(products.values_list("asin", flat=True))
        for product in product_data["products"]:
            if product["asin"] in existing_asins:
                continue
            else:
                Product.objects.create(
                    seller=seller,
                    asin=product["asin"],
                    sku=product["sku"],
                    title=product["title"],
                    image=product["image"],
                    price=product["price"],
                    cost=product["cost"],
                    inventory_available=product["inventory"]["available"],
                    inventory_reserved=product["inventory"]["reserved"],
                    inventory_inbound=product["inventory"]["inbound"],
                    units_sold=product["sales"]["units_sold"],
                    gross_revenue=product["sales"]["gross_revenue"],
                    ad_spend=product["advertising"]["spend"],
                    ad_clicks=product["advertising"]["clicks"],
                    ad_orders=product["advertising"]["orders"],
                    acos=product["advertising"]["acos"],
                    roas=product["advertising"]["roas"],
                    amazon_referral_fee=product["fees"]["amazon_referral_fee"],
                    fba_fee=product["fees"]["fba_fee"],
                    storage_fee=product["fees"]["storage_fee"],
                    advertising_fee=product["fees"]["advertising_fee"],
                    total_fees=product["fees"]["total_fees"],
                    cogs=product["profit"]["cogs"],
                    net_profit=product["profit"]["net_profit"],
                    margin=product["profit"]["margin"],
                    status=product["asin"]
                )
        context.update({
            "products":products
        })
        return context