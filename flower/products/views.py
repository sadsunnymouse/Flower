from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, SubCategory, Product
from django.contrib.auth.decorators import login_required
from .forms import ProductAddForm
from django.contrib import messages
from django.http import JsonResponse
from favorites.models import Favorite
from carts.models import CartItem,Cart

def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(
        subcategory__category=category,
        available=True  # Уже фильтрует по доступности
    ).select_related('subcategory')

    cart_items = {}
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = {str(item.product.id): item.quantity for item in cart.items.all()}
    
    context = {
            'category': category,
            'products': products,
            'cart_items': cart_items,
            'favorite_products': Favorite.objects.filter(user=request.user).values_list('product', flat=True) if request.user.is_authenticated else []
        }
    return render(request, 'products/category.html', context)

def subcategory_view(request, category_id, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id, category_id=category_id)
    products = Product.objects.filter(
        subcategory=subcategory,
        available=True  # Уже фильтрует по доступности
    )
    cart_items = {}
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = {str(item.product.id): item.quantity for item in cart.items.all()}
    
    context = {
        'category': subcategory.category,
        'subcategory': subcategory,
        'products': products,
        'cart_items': cart_items,
        'favorite_products': Favorite.objects.filter(user=request.user).values_list('product', flat=True) if request.user.is_authenticated else []
    }
    
    return render(request, 'products/subcategory.html', context)

# Исправлено: добавлена фильтрация по available=True
def show_products(request):
    products = Product.objects.filter(available=True)  # Фильтр по доступности
    cart_items = {}
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = {str(item.product.id): item.quantity for item in cart.items.all()}
    
    context = {
        'products': products,
        'cart_items': cart_items,
        'favorite_products': Favorite.objects.filter(user=request.user).values_list('product', flat=True) if request.user.is_authenticated else []
    }
    return render(request, 'products/show_products.html', context)

@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request,"Access is prohibited. Only administrators can add products")
        return redirect('products')
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            
            messages.success(request, "The product was successfully added")
            return redirect('')
    else:

        form = ProductAddForm()
    
    return render(request, 'products/add_product.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Получаем текущую историю из куки
    history = request.COOKIES.get('product_history', '')
    history_ids = history.split(',') if history else []

    # Добавляем текущий товар (если его еще нет в истории)
    if str(product.id) not in history_ids:
        history_ids.insert(0, str(product.id))  # Добавляем в начало
        history_ids = history_ids[:10]  # Ограничиваем 10 последними товарами

    cart_items = {}
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = {str(item.product.id): item.quantity for item in cart.items.all()}
    

    # Формируем ответ
    response = render(request, 'products/product_detail.html', {
        'product': product,
        'cart_items': cart_items,
        'favorite_products': Favorite.objects.filter(user=request.user).values_list('product', flat=True) if request.user.is_authenticated else []
    })

    # Устанавливаем куку с обновленной историей (30 дней хранения)
    response.set_cookie(
        'product_history',
        ','.join(history_ids),
        max_age=30 * 24 * 60 * 60,  # 30 дней
        httponly=True
    )

    return response
