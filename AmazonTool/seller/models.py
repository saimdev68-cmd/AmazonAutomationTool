from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class Seller(models.Model):
    times = [
        ("eastern","Eastern (EST)"),
        ("central","Central (CST)"),
        ("mountain","Mountain (MST)"),
        ("pacific","Pacific (PST)"),
        ("gmt","GMT")
    ]


    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="seller")
    seller_id = models.CharField(max_length=100,unique=True,help_text="Amazon Seller/Merchant ID",)
    timezone = models.CharField(max_length=30,choices=times,default="gmt",null=True)
    business_name = models.CharField(max_length=255)
    commision_rate = models.DecimalField(max_digits=12,decimal_places=1,default=20.0)
    amazon_joined_date = models.DateTimeField(null=True,blank=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
        db_table = "sellers"

    def __str__(self):
        return f"{self.business_name} ({self.seller_id})"
    

class Product(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE,related_name="products")
    sku = models.CharField(max_length=100,db_index=True)
    title = models.CharField(max_length=500)
    image = models.ImageField("products/",blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    cost = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.sku} - {self.title}"

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    purchase_date = models.DateField()

    class Meta:
        db_table = "orders"
        ordering = ["-purchase_date"]

    def __str__(self):
        return self.user.email


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    seller = models.ForeignKey(Seller,on_delete=models.SET_NULL,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fees = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fba_fees = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ads_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_ad_order = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order} - {self.seller}"
    
    def save(self, *args, **kwargs):
        if self.product:
            self.price = self.product.price
            self.cost = self.product.cost
            if not self.seller:
                self.seller = self.product.seller
        if self.seller:
            self.fees = (self.price * self.quantity * self.seller.commision_rate ) / Decimal("100")
        if not self.is_ad_order:
            self.ads_cost = Decimal("0.00")
        super().save(*args, **kwargs)
    
class Campaign(models.Model):

    class Status(models.TextChoices):

        ACTIVE = "active" , "Active"
        PAUSED = "paused", "Paused"

    class CampaignType(models.TextChoices):

        PRODUCT = "product", "Sponsored Products"
        BRAND = "brand", "Sponsored Brands"
        DISPLAY = "display", "Sponsored Displays"

    seller = models.ForeignKey(Seller,on_delete=models.CASCADE,related_name="campaigns")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20,choices=CampaignType.choices,default=CampaignType.PRODUCT)
    status = models.CharField(max_length=20 , choices=Status.choices , default= Status.ACTIVE)
    budget = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    amazon_campaign_id = models.CharField(null=True,blank=True)
    target_acos =  models.PositiveIntegerField()
    ppc_spend = models.IntegerField(default=0)
    ppc_sales = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    ctr = models.DecimalField(max_digits=8,decimal_places=1,default=0)
    bid = models.DecimalField(max_digits=8,decimal_places=2,default=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def ppc_acos(self):
        if self.ppc_sales > 0:
            return round((self.ppc_spend / self.ppc_sales) * 100 ,1)
        return 0.0

    class Meta:
        db_table = "campaign"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name