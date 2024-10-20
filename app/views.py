from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from .models import Product, Customer, Cart, Order
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.db.models import F, Q, Count
from django.core.exceptions import MultipleObjectsReturned
import logging
from django.views.decorators.http import require_POST
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import OrderPlaced

# Create your views here.
def home(request):
    return render(request,'testapp/home.html')

def about(request):
    return render(request,'testapp/about.html')

def contact(request):
    return render(request,'testapp/contact.html')




class category_view(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'testapp/category.html', locals())


class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "testapp/productdetail.html", locals()) 


class customerregistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'testapp/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully.")
        else:
            messages.warning(request, "Invalid Input Data.")
        return render(request, 'testapp/customerregistration.html', locals())       


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'testapp/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            pincode = form.cleaned_data['pincode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, pincode=pincode)
            reg.save()
            messages.success(request, "Congratulations! Profile saved successfully.")
        else:
            messages.warning(request, "Invalid Input Data.")
        return render(request, 'testapp/profile.html', locals())      


def address(request):
    try:
        add = Customer.objects.filter(user=request.user)
    except Exception as e:
        print(f"Error retrieving addresses: {e}")
        add = []
    return render(request, 'testapp/address.html', locals())


class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'testapp/update.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.pincode = form.cleaned_data['pincode']
            add.save()
            messages.success(request, "Congratulations! Profile updated successfully.")
        else:
            messages.warning(request, "Invalid Input Data.")    
        return redirect("address")


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    cart_items = Cart.objects.filter(product=product, user=user)
    if cart_items.exists():
        cart_item = cart_items.first()
        cart_item.quantity = F('quantity') + 1
        cart_item.save()
    else:
        Cart.objects.create(user=user, product=product, quantity=1)
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = sum(p.quantity * p.product.discounted_price for p in cart)
    totalamount = amount + 40  # Shipping cost
    return render(request, 'testapp/addcart.html', locals())


class CheckoutView(TemplateView):
    template_name = 'testapp/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = Cart.objects.filter(user=user)
        totalamount = sum(item.quantity * item.product.discounted_price for item in cart)
        for item in cart:
            item.total_price = item.quantity * item.product.discounted_price
        context['cart'] = cart
        context['totalamount'] = totalamount
        return context




def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user

        cart_item = get_object_or_404(Cart, product_id=prod_id, user=user)
        cart_item.quantity += 1
        cart_item.save()

        cart = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart)
        totalamount = amount + 40  # Shipping cost

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user

        cart_item = get_object_or_404(Cart, product_id=prod_id, user=user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

            cart = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40  # Shipping cost

            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': totalamount,
            }
        else:
            cart_item.delete()
            cart = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40  # Shipping cost

            data = {
                'quantity': 0,
                'amount': amount,
                'totalamount': totalamount,
            }
        return JsonResponse(data)



def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        
        if not prod_id:
            return JsonResponse({'error': 'Product ID not provided'}, status=400)
        
        if not user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=403)
        
        try:
            cart_item = get_object_or_404(Cart, product_id=prod_id, user=user)
            cart_item.delete()

            cart = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40  # Shipping cost

            data = {
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)













class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value = p.quantity*p.product.discounted_price
            famount=famount+value
        totalamount=famount+40    
        

        return render(request, 'testapp/checkout.html',locals())





def order_success(request):
    return render(request, 'order_success.html')


def process_order(request):
    # Your order processing logic here
    
    # Redirect to the success page after processing
    return redirect('order_success')