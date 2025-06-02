from django.db import models
from django.urls import reverse

class Category(models.Model):
    """Main product categories"""
    name = models.CharField(max_length=100, verbose_name='Category Name')
    description = models.TextField(blank=True, verbose_name='Category Description')
    image = models.ImageField(
        upload_to='category/', 
        blank=True, 
        verbose_name='Category Image'
    )
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.id})


class SubCategory(models.Model):
    """Product subcategories"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                               related_name='subcategories', verbose_name='Category')
    name = models.CharField(max_length=100, verbose_name='Subcategory Name')
    description = models.TextField(blank=True, verbose_name='Subcategory Description')
    image = models.ImageField(
        upload_to='subcategory/', 
        blank=True, 
        verbose_name='Subcategory Image'
    )
    
    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('subcategory', kwargs={
            'category_id': self.category.id,
            'subcategory_id': self.id
        })


class Product(models.Model):
    """Product model"""
    name = models.CharField(max_length=255, verbose_name='Product Name')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, 
                                   related_name='products', verbose_name='Subcategory')
    description = models.TextField(blank=True, verbose_name='Product Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity in Stock')
    image = models.ImageField(
        upload_to='products/', 
        blank=True, 
        verbose_name='Product Image'
    )
    available = models.BooleanField(default=True, verbose_name='Available')
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (Qty: {self.quantity})"
    
    def save(self, *args, **kwargs):
        """Автоматически обновляем available при изменении quantity"""
        if self.quantity == 0:
            self.available = False
        else:
            self.available = True
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_id': self.id})
# Create your models here.
