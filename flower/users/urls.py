from django.urls import path
from . import views
app_name = "users"
urlpatterns = [
    path('registration/',views.registration, name='registration'),
     path('logout/',views.logout_view, name='logout'),
    path('login/',views.login_user, name='login')
    ]