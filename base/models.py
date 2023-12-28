from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
class Client(AbstractUser):
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=50, null=True)
    avatar = models.ImageField(default='avatar.svg')
    password = models.CharField(max_length=255, null=True)

    companies_list = models.ManyToManyField('Company', related_name='clients')
    groups = None
    user_permissions = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.username

class Company(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=10, null=True)
    avatar = models.ImageField(default='avatar.svg')
    password = models.CharField(max_length=255, null=True)

    our_clients = models.ManyToManyField(Client, related_name='companies')
    groups = None
    user_permissions = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    # Add other fields related to an item

class Order(models.Model):
    title = models.CharField(max_length=150, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    logistics_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    items = models.CharField(max_length=500, null=True)
    quantity = models.IntegerField( null=True)
    status = models.CharField(max_length=150, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title
    
class Notification(models.Model):
    title = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=150, null=True)
    def __str__(self):
        return self.title
    
class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    items = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    price = models.CharField(max_length=150, null=True)
    date_issued = models.DateTimeField(auto_now=True)
    amount_to_be_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)

