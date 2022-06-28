from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from App_shop.models import Product
from .models import Cart, Order
# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_item=Cart.objects.get_or_create(item=item,user=request.user,purchased=False)
    order_qs=Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order=order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity +=1
            order_item[0].save()
            messages.info(request,"The item quantity was added to your cart")
            return redirect('App_shop:home')
        else:
            order.orderitems.add(order_item[0])
            messages.success(request,"Item is added to your cart")
            return redirect('App_shop:home')
    else:
        order=Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request,'This is added to your cart')
        return redirect('App_shop:home')

@login_required
def view_cart(request):
    carts=Cart.objects.filter(user=request.user,purchased=False)
    orders=Order.objects.filter(user=request.user,ordered=False)
    if carts.exists() and orders.exists():
        order=orders[0]
        return render(request,'App_order/cart.html',context={'carts':carts,'order':order})
    else:
        messages.warning(request,"You don't have any item in your cart")
        return redirect('App_shop:home')

@login_required
def remove_from_cart(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item=Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request,'The item was removed from your cart')
            return redirect('App_order:cart')
        else:
            messages.info(request,"This item was not in your cart")
            return redirect('App_shop:home')
    else:
        messages.info(request,"you don't have any active cart")
        return redirect('App_shop:home')

@login_required
def increase_cart(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_items=Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            if order_items.quantity>=1:
                order_items.quantity+=1
                order_items.save()
                messages.success(request,f"{item.name} is successfully added to your cart")
                return redirect('App_order:cart')
        else:
            messages.warning(request,"This item is not in your cart")
            return redirect('App_shop:home')

    else:
        messages.warning(request,"You don't have any active cart")
        return redirect('App_shop:home')

@login_required
def decrease_cart(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_items=Cart.objects.filter(item=item,user=request.user,purchased=False)
            new_order=order_items[0]
            if new_order.quantity>1:
                new_order.quantity-=1
                new_order.save()
                messages.warning(request,'Successfully added item in your cart')
                return redirect('App_order:cart')
            else:
                order.orderitems.remove(new_order)
                new_order.delete()
                messages.warning(request,'Item has been successfully removed from your cart')
                return redirect('App_shop:home')
        else:
            messages.info(request,"you don't have this item in your cart")
            return redirect('App_order:home')
    else:
        messages.warning(request,"you don't have any active cart")
