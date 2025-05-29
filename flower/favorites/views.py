from django.shortcuts import render,get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Favorite
from products.models import Product
from django.contrib import messages

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed', 'message': 'Product removed from favorites.'})
    return JsonResponse({'status': 'added', 'message': 'Product added to favorites.'})

@login_required
def favorite_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "Access is prohibited")
        return redirect('')
    
    favorites = Favorite.objects.filter(user=request.user)
    cart_items = request.session.get('cart', {})
    
    return render(request, 'favorites/favorite_list.html', {
        'favorites': favorites,
        'cart_items': cart_items,
        'favorite_products': [f.product for f in favorites]
    })
