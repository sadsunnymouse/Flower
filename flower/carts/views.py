from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import json
@login_required
def add_to_cart(request):
    if request.method == "POST" and request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Проверка доступного количества товара
        if product.quantity <= 0:
            return JsonResponse({'error': 'Product out of stock'}, status=400)

        # Получаем или создаем корзину
        cart = Cart.get_or_create_cart(user=request.user)

        # Проверяем, есть ли товар уже в корзине
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
        # Check if we can add more items
            if cart_item.quantity >= product.quantity:
                return JsonResponse({'error': 'Maximum available quantity reached'}, status=400)
            cart_item.quantity += 1
            cart_item.save()
        
        total_items = cart.total_items()

        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity,
            'product_id': product.id,
            'total_items': total_items,
            'cart_items': {str(item.product.id): item.quantity for item in cart.items.all()}
        })

@login_required
def view_cart(request):
    cart= Cart.get_or_create_cart(user=request.user)
    cart_items = cart.items.all().select_related('product')
    total_price = cart.total_price()
    
    return render(request, 'carts/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
import logging
logger = logging.getLogger(__name__)
@login_required
def update_cart_item(request, item_id):
    logger.info(f"Request data: {request.POST}")
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        try:
            # Получаем данные из request.POST вместо request.body
            new_quantity = int(request.POST.get('quantity', 1))
            
            if new_quantity > cart_item.product.quantity:
                return JsonResponse({
                    'error': f'Maximum available quantity is {cart_item.product.quantity}'
                }, status=400)
                
            cart_item.quantity = new_quantity
            cart_item.save()
            
            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'item_total': str(cart_item.total_price()),
                'cart_total': str(cart_item.cart.total_price()),
                'total_items': cart_item.cart.total_items()
                })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart = cart_item.cart
    cart_item.delete()
    
    return JsonResponse({
        'success': True,
        'cart_total': cart.total_price(),
        'total_items': cart.total_items()
        })
