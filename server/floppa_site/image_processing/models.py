from django.db import models
from django.core.files import File
from pathlib import Path


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class NN(models.Model):
    name      = models.CharField(max_length=64)
    thumbnail = models.ImageField(upload_to = 'uploads/')
    categories = models.ManyToManyField(Category)

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

    # defect type
    category  = models.ForeignKey(Category, models.SET_NULL, null=True)

    # detail name
    detail_name = models.CharField(max_length=64, null=True)

    def create_new(name, image_path, nn_pk):
        nn = NN.get(pk = nn_pk)
        tmp = NNImage(name = name, nn = nn)
        tmp.thumbnail.save(name + Path(image_path).suffix,
                           File(open(image_path, 'rb')))
        return tmp

    def __str__(self):
        return self.path


class NNImageMarkup(models.Model):
    image = models.ForeignKey(NNImage, on_delete=models.CASCADE)
    x1 = models.PositiveSmallIntegerField()
    y1 = models.PositiveSmallIntegerField()
    x2 = models.PositiveSmallIntegerField()
    y2 = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.image.name}. ({self.x1},{self.y1}) ({self.x2},{self.y2})"
