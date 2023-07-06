from django.db import models
from django.contrib.auth.models import User
from pathlib import PurePath
import random
from django.core.validators import RegexValidator
from .utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse
from delivery.models import *
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers
import json
import requests

def get_filename_ext(filepath):
    name = PurePath(filepath).name
    ext  =  PurePath(filepath).suffix
    return name, ext

def upload_image_path(instance, filename):
    new_filename   = random.randint(1,3910209312)
    name, ext      = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "products/{final_filename}".format(final_filename=final_filename)


def unique_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)







class Collection(models.Model):
    name   = models.CharField(max_length=255)
    slug   = models.SlugField(max_length=128,blank=True,null=True)
    def __str__(self):
        return self.name

pre_save.connect(unique_slug_pre_save_receiver, sender=Collection)




class Product(models.Model):
    name = models.CharField(max_length=255)
    slug   = models.SlugField(max_length=128,blank=True,null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True)
    image       = models.ImageField(upload_to=upload_image_path,null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'product_slug':self.slug})

pre_save.connect(unique_slug_pre_save_receiver, sender=Product)



