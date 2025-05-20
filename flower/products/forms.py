from django import forms
from django.forms import ModelForm, TextInput, Textarea, NumberInput, FileInput
from .models import Flowers

class FlowersForm(ModelForm):

    class Meta:
        model = Flowers
        fields = ['name','quantity','price','description','picture']

        widgets= {
            'name' :TextInput(attrs={'class':'custom-form-control','placeholder':'name'}),
            'quantity':NumberInput(attrs={'class':'custom-form-control','placeholder':'quantity'}),
            'price':NumberInput(attrs={'class':'custom-form-control','placeholder':'price'}),
            'description':Textarea(attrs={'class':'custom-form-control','placeholder':'description'}),
            'picture':FileInput(attrs={'class':'custom-form-control','placeholder':'picture'})
        }