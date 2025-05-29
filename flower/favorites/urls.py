from django.urls import path
from .views import toggle_favorite, favorite_list

urlpatterns = [
    path('toggle-favorite/<int:product_id>/', toggle_favorite, name='toggle_favorite'),
    path('', favorite_list, name='favorites'),
]