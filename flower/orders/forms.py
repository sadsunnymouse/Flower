from django import forms

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order  # Используйте модель, если у вас есть поля для заполнения
        fields = ['first_name', 'last_name', 'email', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country']
