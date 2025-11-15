from django.db import models
from django.urls import reverse


class Product(models.Model):
    slug = models.SlugField('Слаг (для URL)', max_length=100, unique=True)
    title = models.CharField('Название', max_length=200)
    price = models.CharField('Цена', max_length=50)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})