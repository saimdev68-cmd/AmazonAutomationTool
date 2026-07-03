from django.contrib import admin
from .models import Seller , Product , Order , OrderItem , Campaign


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "seller_id",
        "user",
        "region",
        "currency",
        "status",
        "created_at",
    )

    list_filter = (
        "region",
        "status",
        "currency",
        "created_at",
    )

    search_fields = (
        "business_name",
        "seller_id",
        "legal_name",
        "user__email",
        "user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "User & Seller",
            {
                "fields": (
                    "user",
                    "seller_id",
                    "business_name",
                    "legal_name",
                    "commision_rate"
                )
            },
        ),
        (
            "Account Settings",
            {
                "fields": (
                    "region",
                    "currency",
                    "timezone",
                    "status",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "metadata",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    ordering = ("-created_at",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "asin",
        "title",
        "seller",
        "price",
        "gross_revenue",
        "net_profit",
        "inventory_available",
        "acos",
        "status",
    )

    list_filter = (
        "seller",
        "status",
        "created_at",
    )

    search_fields = (
        "asin",
        "sku",
        "title",
        "seller__business_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-gross_revenue",
    )

    list_per_page = 25

    fieldsets = (
        (
            "Seller",
            {
                "fields": (
                    "seller",
                )
            },
        ),

        (
            "Product Information",
            {
                "fields": (
                    "asin",
                    "sku",
                    "title",
                    "image",
                    "status",
                )
            },
        ),

        (
            "Pricing",
            {
                "fields": (
                    "price",
                    "cost",
                )
            },
        ),

        (
            "Inventory",
            {
                "fields": (
                    "inventory_available",
                    "inventory_reserved",
                    "inventory_inbound",
                )
            },
        ),

        (
            "Sales",
            {
                "fields": (
                    "units_sold",
                    "gross_revenue",
                )
            },
        ),

        (
            "Advertising",
            {
                "fields": (
                    "ad_spend",
                    "ad_clicks",
                    "ad_orders",
                    "acos",
                    "roas",
                )
            },
        ),

        (
            "Fees",
            {
                "fields": (
                    "amazon_referral_fee",
                    "fba_fee",
                    "storage_fee",
                    "advertising_fee",
                    "total_fees",
                )
            },
        ),

        (
            "Profit",
            {
                "fields": (
                    "cogs",
                    "net_profit",
                    "margin",
                )
            },
        ),

        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False

    fields = (
        "order_item_id",
        "asin",
        "sku",
        "title",
        "quantity_ordered",
        "item_price",
        "item_tax",
        "promotion_discount",
        "item_status",
    )

    readonly_fields = fields

    show_change_link = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "amazon_order_id",
        "seller_id",
        "marketplace",
        "purchase_date",
        "order_status",
        "order_total",
    )

    list_filter = (
        "marketplace",
        "order_status",
        "fulfillment_channel",
    )

    search_fields = (
        "amazon_order_id",
        "seller_id",
    )

    ordering = ("-purchase_date",)

    inlines = [OrderItemInline]


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "seller",
        "type",
        "status",
        "budget",
        "bid",
        "target_acos",
        "ppc_spend",
        "ppc_sales",
        "clicks",
        "ctr",
        "created_at",
    )

    list_filter = (
        "type",
        "status",
        "seller",
        "created_at",
    )

    search_fields = (
        "name",
        "amazon_campaign_id",
        "seller__name",
    )

    readonly_fields = (
        "ctr",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Campaign Information",
            {
                "fields": (
                    "seller",
                    "name",
                    "type",
                    "status",
                    "amazon_campaign_id",
                )
            },
        ),

        (
            "Budget & Optimization",
            {
                "fields": (
                    "budget",
                    "bid",
                    "target_acos",
                    "ctr",
                )
            },
        ),

        (
            "Performance Metrics",
            {
                "fields": (
                    "ppc_spend",
                    "ppc_sales",
                    "clicks",
                )
            },
        ),

        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )