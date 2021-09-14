from django.contrib.auth.views import UserModel
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse



# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
 def get(self, request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  # print(laptops)

  return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'laptops' : laptops})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  item_already_added = False
  if request.user.is_authenticated:
    item_already_added = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    # print(item_already_added)
  return render(request, 'app/productdetail.html', {'product': product, 'item_already_added': item_already_added})

@login_required
def add_to_cart(request):
  user = request.user
  product_id = request.GET.get('prod_id')
  # print(product_id)
  product = Product.objects.get(id=product_id)
  Cart(user=user, product=product).save()

  return redirect('/cart')

@login_required
def show_cart(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    # print(cart)
    amount = 0.0
    shipping_amount = 100.0
    totalamount = 0.0

    cart_product = [p for p in Cart.objects.all() if p.user == user]
    # print(cart_product)
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount, 'totalitem':totalitem})
    
    else:
      return render(request, 'app/emptycart.html', {'totalitem': totalitem})
  
  else:
    return render(request, 'app/emptycart.html', {'totalitem': totalitem})

def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")


def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 100.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 100.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		data = {
			'amount':amount,
			'totalamount':amount + shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")





def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

@login_required
def address(request):
  add = Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html', {'add': add, 'active':'btn-primary'})

@login_required
def orders(request):
  op = OrderPlaced.objects.filter(user=request.user) 
  return render(request, 'app/orders.html', {'order_placed': op})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'mi' or data == 'samsung' or data == 'Apple':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 return render(request, 'app/mobile.html', {'mobiles': mobiles})

def laptop(request, data=None):
  # return render(request, 'app/laptop.html')
  if data == None:
    laptops = Product.objects.filter(category='L')
    # print(laptops)
  return render(request, 'app/laptop.html', {'laptops':laptops})


def topwear(request, data=None):
 if data == None:
  topwears = Product.objects.filter(category='TW')
 return render(request, 'app/topwear.html', {'topwears':topwears})

def bottomwear(request, data=None):
 if data == None:
  bottomwear = Product.objects.filter(category='BW')
 return render(request, 'app/bottomwear.html', {'bottomwears': bottomwear})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form': form})

 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  
  if form.is_valid():
    messages.success(request, 'Congratulations, Registered Successfully!!!')
    form.save()
  return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_item = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 100.0
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    totalamount = amount + shipping_amount
  
  return render(request, 'app/checkout.html', {'add':add, 'totalamount': totalamount, 'cart_items': cart_item})

@login_required
def payment_done(request):
	custid = request.GET.get('custid')
	# print("Customer ID", custid)
	user = request.user
	cart = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id = custid)
	# print(customer)
	for c in cart:
		OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
		print("Order Saved")
		c.delete()
		print("Cart Item Deleted")
	return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    form = CustomerProfileForm()
    return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

  def post(self, request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      user = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
      reg.save()
      messages.success(request, 'Congratolations, Profile Updated Successfully!!!')
    return render(request, 'app/profile.html', {'form': form, 'active':'btn-primary'})
     
