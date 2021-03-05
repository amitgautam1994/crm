from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    customer_order_ds = {'orders': orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html', customer_order_ds)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, cust_id):
    customer = Customer.objects.get(id=cust_id)
    orders = customer.order_set.all()
    total_orders = orders.count()
    customer_details = {'customer':customer, 'orders':orders, 'total_orders':total_orders}
    return render(request, 'accounts/customer.html', customer_details)
