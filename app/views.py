from django.shortcuts import render,redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#def home(request):
 #return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):
        totalitem=0
        mobile=Product.objects.filter(category='M')
        laptop=Product.objects.filter(category='L')
        processor=Product.objects.filter(category='CP')
        gpu=Product.objects.filter(category='GP')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',context={'mobile':mobile,'laptop':laptop,'processor':processor,'gpu':gpu,'totalitem':totalitem})


class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id),Q(user=request.user)).exists()
        return render(request,'app/productdetail.html', context={'product':product,'item_already_in_cart': item_already_in_cart})
#def product_detail(request):
# return render(request, 'app/productdetail.html')
@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user ==user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discount_price)
                amount += tempamount
                totalamount=amount+shipping_amount
            return render(request, 'app/addtocart.html', context={'carts':cart, 'totalamount':totalamount,'amount':amount})
        else :
            return render(request,'app/emptycart.html')

def plus_cart(request):
    try:
        if request.method=='GET':
            prod_id=request.GET['prod_id']
            c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity+=1
            c.save()
            amount=0.0
            shipping_amount = 70.0
            cart_product=[p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount=(p.quantity * p.product.discount_price)
                amount += tempamount
                #totalamount=amount+shipping_amount

            data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount,
                }
            return JsonResponse(data)
    except Exception as e:
        print("#"*10, e)
        #return JsonResponse(data)


def minus_cart(request):
    try:
        if request.method=='GET':
            prod_id=request.GET['prod_id']
            c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity-=1
            c.save()
            amount=0.0
            shipping_amount = 70.0
            cart_product=[p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount=(p.quantity * p.product.discount_price)
                amount += tempamount
                #totalamount=amount+shipping_amount

            data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount,
                }
            return JsonResponse(data)
    except Exception as e:
        print("#"*10, e)
        #return JsonResponse(data)

def remove_cart(request):
    try:
        if request.method=='GET':
            prod_id=request.GET['prod_id']
            c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

            c.delete()
            amount=0.0
            shipping_amount = 70.0
            cart_product=[p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount=(p.quantity * p.product.discount_price)
                amount += tempamount
                #totalamount=amount

            data = {
                'amount':amount,
                'totalamount':amount+shipping_amount,
                }
            return JsonResponse(data)
    except Exception as e:
        print("#"*10, e)
        #return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')
@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',context={'add':add,'active':'btn-primary'})
@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)

    return render(request, 'app/orders.html',context={'order_placed':op})

#def change_password(request):
 #return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='SONY' or data=='SAMSUNG':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=="below":
        mobiles=Product.objects.filter(category='M').filter(discount_price__lt=100000)
    elif data=="above":
        mobiles=Product.objects.filter(category='M').filter(discount_price__gt=100000)
    return render(request, 'app/mobile.html',context={'mobiles':mobiles})

#def login(request):
 #return render(request, 'app/login.html')

#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',context={'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',context={'form':form})
@login_required
def checkout(request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discount_price)
                amount += tempamount
            totalamount=amount+shipping_amount        
        return render(request, 'app/checkout.html', context={'add':add, 'totalamount':totalamount,'cart_items':cart_items})
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form, 'active':'btn-primary'})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Profile Updated Successfully')
        return render(request,'app/profile.html',context={'form':form,'active':'btn-primary'})
    

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
