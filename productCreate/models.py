# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from account.models import Profile
from django.http import  HttpResponse
from django.template.defaultfilters import slugify
from django.urls import reverse
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200,blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:ads_list_by_category',
                       args=[self.slug])

class SubCategory(models.Model):
    category = models.ForeignKey('Category',null=True, blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Products(models.Model):
    LABEL_CHOICES = (
        ('N', 'new'),
        ('S', 'sale'),
        ('H', 'hot'),
    )

    STATUS = (
        ('sale', 'Sale'),
        ('new', 'New'),
        ('hot', 'Hot'),
        ('unavailable', 'Unavailable'),)

    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE)
    title =models.CharField( max_length=255)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory,
                             on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS, blank=True, null=True)
    price = models.DecimalField(decimal_places=0,
                                   max_digits=30)
    discount_price = models.DecimalField(decimal_places=0,max_digits=30,blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, null=True, blank=True)
    slug = models.SlugField(max_length=200,blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
    available = models.BooleanField(default=True,blank=True)
    active = models.BooleanField(default=True,blank=True)

    class Meta:
        ordering = ('title',)

    index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:ad_detail', args=[self.id, self.slug])

    def get_add_to_cart_url(self):
        return reverse("cart:add_to_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("cart:remove_from_cart", kwargs={
            'slug': self.slug
        })

    def get_first_image(self):
        images = list(self.images.all())
        return images[0:3] if images else None

    def get_second_image(self):
        images = list(self.images.all())
        return images[0:1] if images else None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Products, self).save(*args, **kwargs)

class ProductsImages(models.Model):
    products = models.ForeignKey(Products,related_name="images", on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='ads/', default='image/no_image.png', null=True, blank=True)

    def get_ordering_queryset(self):
        return self.products.images.all()
