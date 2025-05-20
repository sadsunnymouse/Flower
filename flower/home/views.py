from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request,'home/home.html')

def about(request):
    return render(request,'home/about.html')
