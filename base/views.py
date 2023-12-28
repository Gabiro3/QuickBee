from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import *
from .forms import *
from datetime import datetime
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = Client.objects.get(email=name)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Login credentials')
    context = {'page': page}

    return render(request, 'html/login_register.html', context)
    

def logoutUser(request):
    logout(request)
    return redirect('login')
def logoutUser(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    form = ClientRegistrationForm()
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration!')
    return render(request, 'html/login_register.html', {'form': form})

@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    invoices = Invoice.objects.all()
    companies = Company.objects.all()
    context = {'invoices': invoices, 'orders': orders, 'companies': companies}
    return render(request, 'html/client-view.html', context)

@login_required(login_url='login')
def admin(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'html/admin-me.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = Client.objects.get(id=pk)
    notifications = Notification.objects.all()
    context = {'user': user, 'notifications': notifications}
    return render(request, 'html/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
        else:
            return messages.error(request, "Error in updating the profile!")

    return render(request, 'html/update-user.html', {'form': form})

@login_required(login_url='login')
def createOrder(request):
    form = OrderForm()
    companies = Company.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.status = "pending"
            order.save()
            return redirect('view-orders')
        return messages.error(request, 'Order could not be added!')
    context = {'form': form, 'companies': companies}
    return render(request, 'html/place-order.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('view-orders')
        else:
            messages.error(request, "Something wrong with the new data!")

    return render(request, 'html/update-user.html', {'form': form})

@login_required(login_url='login')
def addCompany(request):
    form = CompanyForm()

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
        else:
            return messages.error("An error occurred", request)
        return redirect('admin')
    context = {'form': form}
    return render(request, 'html/add-company.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    # Use get_object_or_404 to handle the case where the order doesn't exist
    order = get_object_or_404(Order, id=pk, client=request.user)

    if request.method == 'POST':
        order.delete()
        return redirect('view-orders')

    return render(request, 'html/delete.html', {'obj': order})

@login_required(login_url='login')
def viewOrders(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'html/order-view.html', context)

@login_required(login_url='login')
def placeInvoice(request):
    form = InvoiceForm()
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view-invoices')
        else:
            return messages.error(request, 'There was an error in creating your invoice')
    return render(request, 'html/create-invoice.html', {'form': form})


@login_required(login_url='login')
def viewInvoices(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(request, 'html/view-invoices.html', context)


def viewInvoice(request, pk):
    invoice = Invoice.objects.get(id=pk)
    total = round(invoice.items.quantity * invoice.amount_to_be_paid)
    tax = 0.3 * total
    overall = round(total - tax)
    context = {'invoice': invoice, 'total': total, 'tax': tax, 'overall': overall}
    return render(request, 'html/Invoice-main/index.html', context)

@login_required(login_url='login')
def viewCompanies(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'html/view-companies.html', context)

@login_required(login_url='login')
def viewCompany(request, pk):
    company = Company.objects.get(id=pk)
    context = {'company': company}
    return render(request, 'html/Invoice-main/company.html', context)


