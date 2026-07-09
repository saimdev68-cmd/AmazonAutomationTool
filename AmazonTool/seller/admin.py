from django.contrib import admin
from .models import Seller , Product , Order , OrderItem , Campaign

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "seller_id",
        "user",
        "timezone",
        "commision_rate",
    )
    search_fields = (
        "business_name",
        "seller_id",
        "user__username",
        "user__email",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "title",
        "seller",
        "price",
        "cost",
    )
    search_fields = (
        "sku",
        "title",
        "seller__business_name",
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = (
        "seller",
        "price",
        "quantity",
        "cost",
        "fees",
        "is_ad_order",
        "fba_fees",
        "ads_cost"
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "purchase_date",
    )
    search_fields = (
        "user__username",
        "user__email",
    )
    list_filter = ("purchase_date",)
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