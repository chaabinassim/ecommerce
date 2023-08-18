from django.db import models
from pathlib import PurePath
import random

def get_filename_ext(filepath):
    name = PurePath(filepath).name
    ext  =  PurePath(filepath).suffix
    return name, ext

def upload_section_image_path(instance, filename):
    new_filename   = random.randint(1,3910209312)
    name, ext      = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "sections/{section_name}/{final_filename}".format(section_name=instance.name,final_filename=final_filename)



class Section(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200,blank=True,null=True)
    subtitle = models.CharField(max_length=300,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to=upload_section_image_path,blank=True,null=True)

    def __str__(self):
        return self.name
