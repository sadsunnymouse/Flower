from django.urls import path
from . import views

urlpatterns = [
    path('',views.show_products, name='products'),
    path('category/<int:category_id>/', views.category_view, name='category_view'),
    path('category/<int:category_id>/subcategory/<int:subcategory_id>/', 
    views.subcategory_view, name='subcategory_view'),
    path('add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    ]


