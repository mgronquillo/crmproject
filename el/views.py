from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user, allowed_user
from .filters import OrderFilter, ProductFilter
from .forms import OrderForm, CustomerForm, CreateUserForm
from .models import Customer, Product, Order

# Create your views here.
@unauthenticated_user
def registerPage(request):                   
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            messages.success(request, 'Created Account for (' + user + ')')
            return redirect('el-login')
    context = {'form': form}
    return render(request, 'el/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('el-home')
        else:
            messages.info(request, 'There Was An Error, Unable To Login')
    context = {}
    return render(request, 'el/login.html', context)

@login_required(login_url='el-login')
def logoutPage(request):
    logout(request)
    messages.warning(request, 'You Have Been Logged Out')
    return redirect('el-login')


@login_required(login_url='el-login')
@allowed_user(allowed_roles=['admin'])
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    initial = orders.filter(status='INITIAL').count()
    pending = orders.filter(status='PENDING').count()
    ofd = orders.filter(status='OUT FOR DELIVERY').count()
    delivered = orders.filter(status='DELIVERED').count()
    total_orders = orders.count()
    context = {'customers': customers, 
               'orders': orders, 
               'initial': initial,
               'pending': pending,
               'ofd': ofd,
               'delivered': delivered,
               'total_orders': total_orders,
               }
    return render(request, 'el/home.html', context)

@login_required(login_url='el-login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {'products': products,
               'myFilter': myFilter,
               }
    return render(request, 'el/products.html', context)

@login_required(login_url='el-login')
@allowed_user(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = customer.order_set.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context= {'customer': customer,
              'total_order': total_order,
              'orders': orders,
              'myFilter': myFilter,
              }
    return render(request, 'el/customer.html', context)

@login_required(login_url='el-login')
@allowed_user(allowed_roles=['admin'])
def createCustomer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('el-home')
        else:
            messages.warning(request, 'There Was An Error, Unable To Add Customer')
    context = {'form': form}
    return render(request, 'el/customer_form.html', context)

@login_required(login_url='el-login')
@allowed_user(allowed_roles=['admin'])
def updateCustomer(request, pk):
    cx = Customer.objects.get(id=pk)
    form = CustomerForm(instance=cx)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=cx)
        if form.is_valid():
            form.save()
            return redirect('el-home')
        else:
            messages.warning(request, 'There Was An Error, Unable To Update Customer')
    context = {'form': form}
    return render(request, 'el/customer_form.html', context)

@login_required(login_url='el-login')
@allowed_user(allowed_roles=['admin'])
def deleteCustomer(request, pk):
    to_delete = Customer.objects.get(id=pk)
    if request.method == 'POST':
        to_delete.delete()
        return redirect('el-home')
    context = {'to_delete': to_delete}
    return render(request, 'el/delete.html', context)

@login_required(login_url='el-login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3)
    customer = Customer.objects.get(id=pk)
    # queryset=Order.objects.none() ---> removes existing items
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('el-home')
    context = {'formset': formset,
               'customer': customer,
               }
    return render(request, 'el/order_form.html', context)

@login_required(login_url='el-login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('el-home')
    context = {'form': form,
               'order': order,
               }
    return render(request, 'el/update_order.html', context)

@login_required(login_url='el-login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('el-home')
    context = {'to_delete': order}
    return render(request, 'el/delete.html', context)