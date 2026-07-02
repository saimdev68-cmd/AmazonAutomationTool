from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "id",
        "name",
        "vendor",
        "price",
        "cost",
        "created_at",
    )
    list_filter = ("vendor", "created_at")
    search_fields = ("sku", "name")