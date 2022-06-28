from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from App_order.models import Cart

from .forms import BillingForm
from .models import Billing_address
from App_order.models import Order
import socket
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

#for payment
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import requests
# Create your views here.

@login_required
def checkout(request):
    saved_address=Billing_address.objects.get_or_create(user=request.user)
    print(saved_address)
    saved_address=saved_address[0]
    print(saved_address)
    form=BillingForm(instance=saved_address)
    if request.method=='POST':
        form=BillingForm(request.POST,instance=saved_address)
        if form.is_valid():
            form.save()
            form=BillingForm(instance=saved_address)
            messages.success(request,f"Successfully saved addresses!")
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    order_item=order_qs[0].orderitems.all()
    order_total=order_qs[0].get_totals()

    return render(request,'App_payment/checkout.html',context={'form':form,'order_item':order_item,'order_total':order_total,'saved_address':saved_address})



@login_required
def payment(request):
    saved_address=Billing_address.objects.get_or_create(user=request.user)
    saved_address=saved_address[0]
    if not saved_address.is_fully_filled():
        messages.warning(request,f"Address is not fully filled")
        return redirect('App_payment:checkout')
    
    if not request.user.profile.is_fully_filled():
        messages.warning(request,f"Address is not fully filled")
        return redirect('App_login:profile')
    store_id= 'gadge62af4c742ae0c'
    API_KEY='gadge62af4c742ae0c@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_KEY)

    status_url=request.build_absolute_uri(reverse('App_payment:complete'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)


    order_qs=Order.objects.filter(user=request.user)
    print(order_qs)
    order_items=order_qs[0].orderitems.all()
    total_amount=order_qs[0].get_totals()
    order_items_count=order_qs[0].orderitems.count()
    #item_name=order_items.orderitems.item
    #print(item_name)
    current_user=request.user
    mypayment.set_product_integration(total_amount=Decimal(total_amount), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=order_items_count, shipping_method='Courier', product_profile='None')

    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address_1, address2=current_user.profile.address_1, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=saved_address.user, address=saved_address.address, city=saved_address.city, postcode=saved_address.zip_code, country=saved_address.country)

    response_data = mypayment.init_payment()
    
    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def complete(request):
    if request.method=='POST' or request.method=='post':
        payment_data=request.POST
        #print(payment_data)
        status=payment_data['status']
        if status == 'VALID':
            tran_id=payment_data['tran_id']
            val_id=payment_data['val_id']
            #bank_transaction_id=payment_data['bank_tran_id']
            messages.success(request,f"Your Payment completed successfully")
            return HttpResponseRedirect(reverse('App_payment:purchase',kwargs={'val_id':val_id,'tran_id':tran_id}))
        elif status =='FAILED':
            messages.warning(request,f"Your payment Failed! Please Try Again page will redirected soon")
    return render(request,'App_payment/complete.html',context={})


def purchase(request,val_id,tran_id):
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    order=order_qs[0]
    orderId=tran_id
    order.ordered=True
    order.orderId=orderId
    order.paymentId=val_id
    order.save()
    cart_items=Cart.objects.filter(user=request.user,purchased=False)
    for cart in cart_items:
        cart.purchased=True
        cart.save()
    return HttpResponseRedirect(reverse('App_shop:home'))

@login_required
def order(request):
    try:
        orders=Order.objects.filter(user=request.user,ordered=True)
        context={'orders':orders}
    except:
        messages.warning(request,f"You don't have any active order")
        return redirect('App_shop:home')

    return render(request,'App_payment/order.html',context)