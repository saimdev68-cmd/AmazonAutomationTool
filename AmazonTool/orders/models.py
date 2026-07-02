from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from vendor.models import Vendor

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    
    @property
    def total(self):
        return sum(item.sub_total for item in self.items.all())
    

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,related_name="items")
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True,related_name="items")

    product_name = models.CharField(max_length=255) 

    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sub_total = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    net_profit = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    
    created_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        if self.product:
            self.product_name = self.product.name
            # self.price = self.product.price
            # self.cost = self.product.cost

        if self.vendor and self.price:
            self.fees = (
                self.price * self.quantity *
                (self.vendor.commision_rate / 100)
            )
        else:
            self.fees = 0
        self.sub_total = self.price * self.quantity
        self.net_profit = self.sub_total - self.cost - self.fees
        super().save()
