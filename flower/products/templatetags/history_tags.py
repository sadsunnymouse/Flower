from django import template
from products.models import Product

register = template.Library()

@register.filter
def get_product(product_id):
    try:
        return Product.objects.get(id=product_id)
    except (Product.DoesNotExist, ValueError):
        return None

@register.filter
def split(value, delimiter):
    return value.split(delimiter)