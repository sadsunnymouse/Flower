from django.shortcuts import render, redirect
from .models import Flowers
from .forms import FlowersForm
from django.views.generic import DetailView


def show_products(request):
    flowers = Flowers.objects.all()
    return render(request,'products/show_products.html',{'flowers':flowers})

def create(request):
    error = ''
    if request.method == 'POST':
        form = FlowersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('')
        else:
            error = 'It is not valid'
            form = FlowersForm()
            
            
    form = FlowerForm()
    data = {'form': form, 'error': error}
    
    return render(request,'products/create.html',data)


class ProductsDetailView(DetailView):
    model = Flowers
    template_name = 'products/details_view.html'
    context_object_name = 'Flower'
    