from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from products.models import Product

from django.db import transaction

@login_required
@transaction.atomic
def order(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            messages.warning(request, "Your cart is empty")
            return redirect('view_cart')
        
        # Проверяем доступность товаров
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.quantity:
                messages.error(request, f"Not enough stock for {cart_item.product.name}")
                return redirect('view_cart')
        
        # Создаем заказ и уменьшаем количество товаров в одной транзакции
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=cart.total_price()
            )
            
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                
                product = cart_item.product
                product.quantity -= cart_item.quantity
                product.save()
            
            cart.items.all().delete()
        
        messages.success(request, "Order placed successfully!")
        return redirect('order_detail', order_id=order.id)
    
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty")
        return redirect('view_cart')
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
