from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
]