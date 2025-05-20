from django.urls import path
from . import views

urlpatterns = [
    path('',views.show_products, name='products'),
    path('create',views.create, name='create'),
    path('<int:pk>',views.ProductsDetailView.as_view(),name='products-detail')
]