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
        available=True
    ).select_related('subcategory')
    return render(request, 'products/category.html',{'category': category,'products': products})

def subcategory_view(request, category_id, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id, category_id=category_id)
    products = Product.objects.filter(
        subcategory=subcategory,
        available=True
    )
    
    return render(request, 'products/subcategory.html', {
        'category': subcategory.category,
        'subcategory': subcategory,
        'products': products
    })


# Create your views here.
def show_products(request):
    products = Product.objects.all()
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
            return redirect(product.get_absolute_url())
    else:

        form = ProductAddForm()
    
    return render(request, 'products/add_product.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})