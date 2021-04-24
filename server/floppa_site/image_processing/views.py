from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Category
from .models import NN


@login_required
def nn_select(request):
    NNs     = NN.objects.all()
    context = {'NNs': NNs}
    return render(request, 'image_processing/nn_select.html', context)


@login_required
def nn_detail(request, pk):
    nn         = NN.objects.get(pk = pk)
    images     = nn.nnimage_set.all()
    images_qty = images.count()
    parsed_images_qty = images.filter(trained = True).count()
    categories = nn.categories.all()
    context = {"nn":                nn,
               "images":            images,
               "images_qty":        images_qty,
               "parsed_images_qty": parsed_images_qty,
               "categories":        categories}
    return render(request, 'image_processing/nn_detail.html', context)


@login_required
def nn_images_preview(request, pk):
    num_in_rows = 7
    nn = NN.objects.get(pk = pk)
    # возвращаемый массив это массив из строчек каждая из которых состоит
    # из объектов картинок
    images = []
    for i, image in enumerate(nn.nnimage_set.all()):
        if (i % num_in_rows) == 0:
            images.append([])
        images[-1].append(image)
    context = {"nn": nn, "images": images}
    return render(request, 'image_processing/nn_images_preview.html', context)


@login_required
def nn_add_category(request, pk):
    nn = NN.objects.get(pk = pk)
    context = {"nn": nn}
    return render(request, 'image_processing/add_category.html', context)


@login_required
def nn(request):
    NNs = NN.objects.all()
    context = {'NNs': NNs}
    return render(request, 'image_processing/NN.html', context)
