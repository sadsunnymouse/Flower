from .models import Category
from carts.models import Cart
from django.db.models import Sum


def categories(request):
    return {
        'categories': Category.objects.prefetch_related('subcategories').all()
    }


def cart_total_items(request):
    if request.user.is_authenticated:
        try:
            # Пытаемся получить корзину пользователя
            cart = Cart.objects.get(user=request.user)
            return {'cart_total_items': cart.total_items()}
        except Cart.DoesNotExist:
            # Если корзины нет - возвращаем 0
            return {'cart_total_items': 0}
    return {'cart_total_items': 0}