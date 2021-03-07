from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
# Create your views here

@login_required(login_url="login")
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    customer_order_ds = {'orders': orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html', customer_order_ds)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('login')

        context = {'form': form}
        return render(request, "accounts/register.html", context)
    

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username, password)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Incorrect username or password')
        return render(request, "accounts/login.html")


def logoutUser(request):
    logout(request)
    return redirect('login')


def userPage(request):
    context = {}
    return render(request, 'account/user.html', context)


@login_required(login_url="login")
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url="login")
def customer(request, cust_id):
    customer = Customer.objects.get(id=cust_id)
    orders = customer.order_set.all()
    total_orders = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    customer_details = {'customer':customer, 'orders':orders, 'total_orders':total_orders, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', customer_details)


@login_required(login_url="login")
def createOrder(request, cust_id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=cust_id)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url="login")
def updateOrder(request, order_id):
    order = Order.objects.get(id=order_id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url="login")
def deleteOrder(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)
