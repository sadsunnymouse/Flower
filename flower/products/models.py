from django.db import models

class Flowers(models.Model):
    name = models.CharField(max_length=300)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    picture = models.ImageField(upload_to='media', blank=True, null=True)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = 'Flower'
        verbose_name_plural = 'Flowers'


