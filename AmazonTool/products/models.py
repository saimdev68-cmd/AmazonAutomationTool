from django.db import models
from vendor.models import Vendor

# Create your models here.

class Product(models.Model):

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="products"
    )

    sku = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sku} - {self.name}"