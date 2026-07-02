from django.contrib import admin
from .models import Order, OrderItem


# Inline Order Items inside Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "vendor", "product_name", "price", "cost", "quantity", "fees","sub_total","net_profit")
    can_delete = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("id", "user__username")
    inlines = [OrderItemInline]