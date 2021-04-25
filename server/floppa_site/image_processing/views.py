from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Category,NN,NNImage,Category


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
def add_category(request, pk):
    if request.method == "POST":
        category_name = request.POST['category_name']
        nn = NN.objects.get(pk = pk)
        category = Category(name = category_name)
        category.save()
        nn.categories.add(category)
        context = {"nn": nn}
        return render(request, 'image_processing/add_category.html', context)
    else:
        nn = NN.objects.get(pk = pk)
        context = {"nn": nn}
        return render(request, 'image_processing/add_category.html', context)


@login_required
def use(request, pk):
    nn = NN.objects.get(pk = pk)
    # sql_set = nn.nnimage_set.values('category').annotate(total=Count("id")).order_by('category')
    sql_set = (NNImage.objects.all()
               .values('category__name')
               .filter(nn = nn)
               .annotate(total=Count("id"))
               .filter(category__name__isnull=False, total__lt=100))
    # sql_set = Category.objects.all().values('name').filter(nnimage__nn = nn).annotate(total=Count("id"))
    print(sql_set)
    # sql_set = nn.nnimage_set.values('category').annotate(total=Count("category"))
    # nnimages = nn.nnimage_set.all()
    context = {"nn": nn,
               "sql_set": sql_set}
    return render(request, 'image_processing/use.html', context)
    # не готова: меньше 100 фотографий каждой категории
    # готова к обучению: нейронка еще не обучена
    # готова к использованию: нейронка обучена


@login_required
def nn(request):
    NNs = NN.objects.all()
    context = {'NNs': NNs}
    return render(request, 'image_processing/NN.html', context)
