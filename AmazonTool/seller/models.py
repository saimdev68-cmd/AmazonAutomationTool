from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Seller(models.Model):
    class Region(models.TextChoices):
        NA = "NA", "North America"
        EU = "EU", "Europe"
        FE = "FE", "Far East"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SUSPENDED = "suspended", "Suspended"


    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="seller")
    seller_id = models.CharField(max_length=100,unique=True,help_text="Amazon Seller/Merchant ID",)
    business_name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255,blank=True,null=True)
    region = models.CharField(max_length=5,choices=Region.choices,default=Region.NA)
    currency = models.CharField(max_length=10,default="USD")
    timezone = models.CharField(max_length=100,default="UTC")
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)

    metadata = models.JSONField(default=dict,blank=True)
    amazon_joined_date = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
        db_table = "sellers"

    def __str__(self):
        return f"{self.business_name} ({self.seller_id})"
    

class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SUPPRESSED = "suppressed", "Suppressed"

    seller = models.ForeignKey(Seller,on_delete=models.CASCADE,related_name="products")
    asin = models.CharField(max_length=20,unique=True)
    sku = models.CharField(max_length=100,db_index=True)
    title = models.CharField(max_length=500)
    image = models.ImageField("products/",blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    cost = models.DecimalField(max_digits=10,decimal_places=2)
    inventory_available = models.IntegerField(default=0)
    inventory_reserved = models.IntegerField(default=0)
    inventory_inbound = models.IntegerField(default=0)
    units_sold = models.IntegerField(default=0)
    gross_revenue = models.PositiveIntegerField(default=0)
    ad_spend = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    ad_clicks = models.IntegerField(default=0)
    ad_orders = models.IntegerField( default=0 )
    acos = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    roas = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    amazon_referral_fee = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    fba_fee = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    storage_fee = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    advertising_fee = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    total_fees = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    cogs = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    net_profit = models.IntegerField(default=0)
    margin = models.DecimalField(max_digits=5,decimal_places=1,default=0)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku} - {self.title}"