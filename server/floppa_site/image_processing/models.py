from django.db import models
from django.core.files import File
from pathlib import Path


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class NN(models.Model):
    name       = models.CharField(max_length=64)
    thumbnail  = models.ImageField(upload_to = 'uploads/')
    categories = models.ManyToManyField(Category)
    trained    = models.BooleanField(default=False)

    def create_new(name, image_path):
        # get extension
        tmp = NN(name = name)
        tmp.thumbnail.save(name + Path(image_path).suffix,
                           File(open(image_path, 'rb')))
        return tmp

    def __str__(self):
        return self.name


class NNImage(models.Model):
    name      = models.CharField(max_length=64)
    thumbnail = models.ImageField(upload_to = 'nnimage_uploads')
    nn        = models.ForeignKey(NN, on_delete=models.CASCADE)
    trained   = models.BooleanField()

    # detail name
    detail_name = models.CharField(max_length=64, null=True)

    def create_new(name, image_path, nn, category=None, detail_name=None, trained=False):
        tmp = NNImage(name = name, nn = nn, trained = trained)
        tmp.thumbnail.save(name + Path(image_path).suffix,
                           File(open(image_path, 'rb')))
        return tmp

    def __str__(self):
        return self.name


class NNImageMarkup(models.Model):
    image = models.ForeignKey(NNImage, on_delete=models.CASCADE)
    x1 = models.PositiveSmallIntegerField()
    y1 = models.PositiveSmallIntegerField()
    x2 = models.PositiveSmallIntegerField()
    y2 = models.PositiveSmallIntegerField()

    # defect type
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.image.name}. ({self.x1},{self.y1}) ({self.x2},{self.y2})"
