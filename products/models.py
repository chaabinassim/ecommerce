from django.db import models
from django.contrib.auth.models import User
from pathlib import PurePath
import random
from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator
from .utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse
from delivery.models import *
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers
import json
import requests
from decimal import Decimal

def get_filename_ext(filepath):
    name = PurePath(filepath).name
    ext  =  PurePath(filepath).suffix
    return name, ext

def upload_image_path(instance, filename):
    new_filename   = random.randint(1,3910209312)
    name, ext      = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "products/{collection_name}/{final_filename}".format(collection_name=instance.collection.name,final_filename=final_filename)


def upload_collection_image_path(instance, filename):
    new_filename   = random.randint(1,3910209312)
    name, ext      = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "collections/{final_filename}".format(final_filename=final_filename)


def upload_thumbnail_image_path(instance, filename):
    new_filename   = random.randint(1,3910209312)
    name, ext      = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "thumbnail/{product}/{final_filename}".format(product=instance.product.name,final_filename=final_filename)

def unique_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)




class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name   = models.CharField(max_length=255,blank=True,null=True)# change on production
    slug   = models.SlugField(max_length=128,blank=True,null=True)
    description   = models.CharField(max_length=255,blank=True,null=True)
    image       = models.ImageField(upload_to=upload_collection_image_path,null=True, blank=True)
    is_featured = models.BooleanField(default=False,null=True, blank=True)

    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('collection-detail',kwargs={'collection_slug':self.slug})

pre_save.connect(unique_slug_pre_save_receiver, sender=Collection)




class Product(models.Model):
    name = models.CharField(max_length=255)
    slug   = models.SlugField(max_length=128,blank=True,null=True)
    description = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True,blank=True,)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True,related_name='products')
    image       = models.ImageField(upload_to=upload_image_path,null=True, blank=True)
    in_stock   = models.BooleanField(null=True, blank=True,default=True)
    is_featured = models.BooleanField(default=False,null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True,
        validators=[
            MinValueValidator(0),  # Minimum value of 0
            MaxValueValidator(100),  # Maximum value of 100
        ]
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'product_slug':self.slug})
    

    @property
    def discounted_price(self):
        if self.discount is None:
            return self.price
        discount_percentage = Decimal(str(self.discount))
        discounted_price = self.price * (1 - discount_percentage / 100)
        return discounted_price
    
    
        

pre_save.connect(unique_slug_pre_save_receiver, sender=Product)



class Thumbnail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='thumbnails')
    thumbnail = models.ImageField(upload_to=upload_thumbnail_image_path)

    def __str__(self):
        return f"thumbnail for product :{self.product.name}"
