from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, Payment, OrderPlaced
from . form import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
import razorpay




def home(request):
    return render(request, "index.html")
def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")




class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'category.html',locals())

class CategoryTitle(View):
    def get(self, request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'category.html',locals())
class ProductDetails(View):
    def get(self,request,pk):
        product_details = Product.objects.get(pk=pk)
        return render(request, 'productdetail.html', locals())

class CustomerRegister(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return  render(request,'CustomerRegiser.html',locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully!")
        else:
            messages.warning(request, "Invalid input data")
        return render(request, 'CustomerRegiser.html', locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm(request.POST)
        return render(request, 'profile.html', {'form': form})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save successfully!")
        else:
            messages.warning(request, "Invalid input data")

        return render(request,'profile.html',locals())

def add_to_cart(request):
    user = request.user
    product = Product.objects.get(id=request.GET.get('prod_id'))
    Cart(user=user, product=product).save()
    return redirect("/cart")





def show_card(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity * p.product.discount_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'addtocard.html',locals())


class checkout(View):
    def get(self, request):
        user = request.user
        add = Cart.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discount_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)

        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':  # Check if the order was successfully created
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
            )
            payment.save()

        return render(request, 'checkout.html', locals())

def create_razorpay_order(request):
    if request.method == 'POST':
        # Initialize the Razorpay client with your API key
        client = razorpay.Client(auth=("rzp_test_X8JTUIMP8JBwEd", "7YejyN6j0Ci5ScBxN6RHlPc9"))

        # Create a Razorpay order
        data = {
            'amount': 1000,  # Amount in paise (e.g., 1000 paise = ₹10)
            'currency': 'INR',
            'receipt': 'order_rcptid_11',
            'payment_capture': 1  # Auto-capture payment
        }
        order = client.order.create(data=data)

        # Pass the Razorpay order ID to the template
        context = {
            'order_id': order['id'],
            'amount': order['amount'],
        }

        return render(request, 'checkout.html', locals())

    return render(request, 'checkout.html')

def paymentdone(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment. save()
    cart=Cart.objects.filter (user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c. quantity, payment=payment).save()
        c.delete()
    return redirect("/orders")

def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q (user=request.user))
        c.quantity +=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        totalamount = amount + 40



        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def minuscart(request):
        if request.method == 'GET':
            prod_id = request.GET.get('prod_id')
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity -= 1
            c.save()
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discount_price
                amount = amount + value
            totalamount = amount + 40

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)

def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        totalamount = amount + 40

        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def search(request):
    query = request.GET['search']
    totalitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    products = Product.objects.filter(Q(title__icontains=query))

    return render(request, 'search.html', locals())
