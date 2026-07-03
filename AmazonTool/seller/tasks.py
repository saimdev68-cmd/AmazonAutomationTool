import json
from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Product, Order, OrderItem , Campaign

User = get_user_model()


@shared_task
def sync_seller_data(user_id):

    user = User.objects.get(id=user_id)
    seller = user.seller

    with open("seller/data/products.json") as f:
        product_data = json.load(f)

    with open("seller/data/orders.json") as f:
        order_data = json.load(f)

    with open("seller/data/order_items.json") as f:
        order_item_data = json.load(f)

    # products
    for product in product_data["products"]:
        Product.objects.update_or_create(
            seller=seller,
            asin=product["asin"],
            defaults={
                "sku": product["sku"],
                "title": product["title"],
                "image": product["image"],
                "price": product["price"],
                "cost": product["cost"],

                "inventory_available":
                    product["inventory"]["available"],
                "inventory_reserved":
                    product["inventory"]["reserved"],
                "inventory_inbound":
                    product["inventory"]["inbound"],

                "units_sold":
                    product["sales"]["units_sold"],
                "gross_revenue":
                    product["sales"]["gross_revenue"],

                "ad_spend":
                    product["advertising"]["spend"],
                "ad_clicks":
                    product["advertising"]["clicks"],
                "ad_orders":
                    product["advertising"]["orders"],
                "acos":
                    product["advertising"]["acos"],
                "roas":
                    product["advertising"]["roas"],

                "amazon_referral_fee":
                    product["fees"]["amazon_referral_fee"],
                "fba_fee":
                    product["fees"]["fba_fee"],
                "storage_fee":
                    product["fees"]["storage_fee"],
                "advertising_fee":
                    product["fees"]["advertising_fee"],
                "total_fees":
                    product["fees"]["total_fees"],

                "cogs":
                    product["profit"]["cogs"],
                "net_profit":
                    product["profit"]["net_profit"],
                "margin":
                    product["profit"]["margin"],

                "status":
                    product["status"],
            }
        )

    # orders
    for order in order_data["orders"]:
        Order.objects.update_or_create(
            seller=seller,
            amazon_order_id=order["amazon_order_id"],
            defaults={
                "marketplace":
                    order_data["marketplace"],
                "currency":
                    order_data["currency"],
                "purchase_date":
                    order["purchase_date"],
                "order_status":
                    order["order_status"],
                "fulfillment_channel":
                    order["fulfillment_channel"],
                "buyer_country":
                    order["buyer_country"],
                "number_of_items":
                    order["number_of_items"],
                "order_total":
                    order["order_total"],
            }
        )

    orders = {
        o.amazon_order_id: o
        for o in Order.objects.filter(seller=seller)
    }

    # order items
    for item in order_item_data["order_items"]:
        order = orders.get(item["amazon_order_id"])

        if not order:
            continue

        OrderItem.objects.update_or_create(
            order_item_id=item["order_item_id"],
            defaults={
                "order": order,
                "seller_id":
                    order_item_data["seller_id"],
                "marketplace":
                    order_item_data["marketplace"],
                "currency":
                    order_item_data["currency"],
                "asin":
                    item["asin"],
                "sku":
                    item["sku"],
                "title":
                    item["title"],
                "quantity_ordered":
                    item["quantity_ordered"],
                "item_price":
                    item["item_price"],
                "item_tax":
                    item["item_tax"],
                "promotion_discount":
                    item["promotion_discount"],
                "item_status":
                    item["item_status"],
            }
        )

@shared_task
def sync_all_sellers():

    User = get_user_model()

    for user in User.objects.filter(
        seller__isnull=False
    ):
        sync_seller_data.delay(user.id)

@shared_task
def sync_campaigns(user_id):

    user = User.objects.get(id=user_id)
    seller = user.seller

    with open("seller/data/compaign.json") as f:
        campaign_data = json.load(f)

    for campaign in campaign_data["campaigns"]:

        obj, created = Campaign.objects.update_or_create(
            seller=seller,
            amazon_campaign_id=int(campaign["amazon_campaign_id"]),
            defaults={
                "name": campaign["name"],
                "type": campaign["type"],
                "status": campaign["status"],
                "budget": campaign["budget"],
                "target_acos": campaign["target_acos"],
                "ppc_spend": campaign["ppc_spend"],
                "ppc_sales": campaign["ppc_sales"],
                "clicks": campaign["clicks"],
                "ctr":campaign["ctr"]
            }
        )

@shared_task
def sync_all_campaigns():

    for user in User.objects.filter(
        seller__isnull=False
    ):
        sync_campaigns.delay(user.id)