from django import forms
from .models import Product, SubCategory

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'subcategory', 'description', 'price', 'quantity', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Name',
            'subcategory': 'Subcategory',
            'description': 'Description',
            'price': 'Price',
            'quantity': 'Quantity',
            'image': 'Image',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Опционально: можно ограничить выбор подкатегорий
        self.fields['subcategory'].queryset = SubCategory.objects.all()