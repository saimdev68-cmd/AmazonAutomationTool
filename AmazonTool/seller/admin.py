from django.contrib import admin
from .models import Seller


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


from django.contrib import admin
from .models import Product


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