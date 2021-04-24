from django.db import models
from django.core.files import File
from django.conf import settings
from pathlib import Path

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class NN(models.Model):
    name      = models.CharField(max_length=64)
    thumbnail = models.ImageField(upload_to = 'uploads/')

    def create_new(name, image_path):
        # get extension
        tmp = NN(name = name)
        tmp.thumbnail.save(name + Path(image_path).suffix,
                           File(open(image_path, 'rb')))
        return tmp

    def __str__(self):
        return self.name
