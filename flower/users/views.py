from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm
from .forms import LoginUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect

def registration(request):
    if request.user.is_authenticated:
        return redirect('')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return render(request, 'users/register_done.html', {'new_user': new_user})
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form':form})



def login_user(request):
    if request.user.is_authenticated:
        return redirect('about')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('')
            
  
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
