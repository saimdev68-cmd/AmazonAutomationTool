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
    legal_name = models.CharField(max_length=255,blank=True,null=True)
    region = models.CharField(max_length=5,choices=Region.choices,default=Region.NA)
    currency = models.CharField(max_length=10,default="USD")
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)
    commision_rate = models.DecimalField(max_digits=12,decimal_places=1,default=20.0)

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
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def gross_revenue_per(self):
        if self.gross_revenue > 0:
            return 100.0
        return 0.0

    @property
    def gross_profit(self):
        return self.gross_revenue - self.cogs - self.total_fees

    def __str__(self):
        return f"{self.sku} - {self.title}"

class Order(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE,related_name="orders")
    marketplace = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    amazon_order_id = models.CharField(max_length=30,unique=True)
    purchase_date = models.DateTimeField()
    order_status = models.CharField(max_length=30)
    fulfillment_channel = models.CharField(max_length=20,blank=True,null=True)
    buyer_country = models.CharField(max_length=5,blank=True,null=True)
    number_of_items = models.PositiveIntegerField(default=0)
    order_total = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"
        ordering = ["-purchase_date"]
        indexes = [
            models.Index(fields=["seller_id"]),
            models.Index(fields=["marketplace"]),
            models.Index(fields=["purchase_date"]),
            models.Index(fields=["order_status"]),
        ]

    def __str__(self):
        return self.amazon_order_id


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    seller_id = models.CharField(max_length=30, db_index=True)
    marketplace = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    order_item_id = models.CharField(max_length=30,unique=True)
    asin = models.CharField(max_length=20, db_index=True)
    sku = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=500)
    quantity_ordered = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=12,decimal_places=2)
    item_tax = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    promotion_discount = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    item_status = models.CharField(max_length=30)

    class Meta:
        db_table = "order_items"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["asin"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["seller_id"]),
            models.Index(fields=["item_status"]),
        ]

    def __str__(self):
        return f"{self.order.amazon_order_id} - {self.sku}"
    
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