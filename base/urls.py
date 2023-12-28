from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('client/', views.home, name="home"),
    path('me/', views.admin, name="admin"),

    path('profile/<str:pk>', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),

    path('add-company/', views.addCompany, name="add-company"),
    path('companies/', views.viewCompanies, name="view-companies"),
    path('company/<str:pk>/', views.viewCompany, name="view-company"),

    path('add-order/', views.createOrder, name="add-order"),
    path('delete-order/<str:pk>/', views.deleteOrder, name="delete-order"),
    path('orders/', views.viewOrders, name="view-orders"),
    path('update-order/<str:pk>/', views.updateOrder, name="update-order"),

    path('invoices/', views.viewInvoices, name="view-invoices"),
    path('invoice/<str:pk>/', views.viewInvoice, name="view-invoice"),
    path('new-invoice/', views.placeInvoice, name="create-invoice"),
]