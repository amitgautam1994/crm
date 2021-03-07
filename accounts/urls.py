"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('user/<str:cust_id>', views.userPage, name='user')

    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:cust_id>', views.customer, name='customer'),
    path('create_order/<str:cust_id>', views.createOrder, name='create_order'),
    path('update_order/<str:order_id>', views.updateOrder, name='update_order'),
    path('delete_item/<str:order_id>', views.deleteOrder, name='delete_order'),
]
