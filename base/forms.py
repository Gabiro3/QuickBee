from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User
from django import forms

class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['username', 'email', 'phone_number', 'category', 'password1', 'password2']

class CompanyRegistrationForm(UserCreationForm):
    class Meta:
        model = Company
        fields = ['username', 'email', 'phone_number', 'category']

class UserForm(ModelForm):
    class Meta:
        model = Client
        fields = ['username', 'email', 'avatar', 'category', 'phone_number']
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['title','logistics_company', 'items', 'quantity']

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['username', 'email', 'phone_number']
class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'items', 'amount_to_be_paid']