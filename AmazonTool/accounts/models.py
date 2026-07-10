from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.

class User(AbstractUser):
    
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    pending_email = models.EmailField(null=True,blank=True)

    otp = models.CharField(max_length=255,null=True,blank=True)
    otp_created_at = models.DateTimeField(null=True,blank=True)
    otp_attempt = models.PositiveIntegerField(default=0)
    otp_block_time = models.DateTimeField(null=True,blank=True)

    objects = UserManager()
    
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []
    
    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"

    def __str__(self):
        return self.email