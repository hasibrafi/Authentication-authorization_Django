from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . decorators import *
from . models import *
from . forms import *
from . filters import *

# Create your views here.

@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin'])
def index(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers':customers, 'total_customers':total_customers, 'total_orders':total_orders, 
               'delivered':delivered, 'pending': pending }

    return render (request,'index.html', context)


@unauthenticated_user
def registration(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account created for :'+ user + '!')
            return redirect('login')

    context = {'form':form}
    return render (request,'registration.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or Password is INCORRECT!')

    context = {}
    return render (request,'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def userPage(request):
    context = {}
    return render(request,'user.html',context)


@login_required(login_url='login')     
def customers(request, pk="1"):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'orders_count': orders_count, 'myFilter': myFilter }
    return render (request,'customers.html', context)

@login_required(login_url='login') 
def products(request):
    products = Product.objects.all()
    return render (request,'products.html',{'products':products})
 
@login_required(login_url='login') 
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet (queryset= Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render (request, 'order_form.html', context)

@login_required(login_url='login') 
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}

    return render(request, 'order_form.html', context)

@login_required(login_url='login') 
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order':order}
    return render(request, 'delete.html', context)

