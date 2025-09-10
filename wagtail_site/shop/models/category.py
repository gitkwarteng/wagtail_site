from django.db import models
from django.urls import reverse
from wagtail.models import Orderable, Page, TranslatableMixin

from wagtail_site.shop.models.base.fields import AutoSlugField


class ProductCategory(TranslatableMixin, Orderable):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, overwrite=True)
    description = models.TextField(blank=True)

    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        if hasattr(self, 'page'):
            return self.page.get_url()
        return reverse('shop:category-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        unique_together = ('translation_key', 'locale')


class Classification(TranslatableMixin, Orderable):
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, overwrite=True)
    description = models.TextField(blank=True)
    pages = models.ManyToManyField(Page, related_name='classifications', limit_choices_to={'live': True})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Classification"
        verbose_name_plural = "Product Classifications"
        unique_together = ('translation_key', 'locale')