import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect
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
    for i, image in enumerate(nn.nnimage_set.all().order_by('trained')):
        if (i % num_in_rows) == 0: images.append([])
        images[-1].append(image)
    context = {"nn": nn, "images": images}
    return render(request, 'image_processing/nn_images_preview.html', context)


@login_required
def add_category(request, pk):
    if request.method == "POST":
        category_name = request.POST['category_name']
        nn = NN.objects.get(pk = pk)
        category, created = Category.get_or_create(name = category_name)
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
    # не готова: меньше 100 фотографий каждой категории
    # готова к обучению: нейронка еще не обучена
    # готова к использованию: нейронка обучена
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


@login_required
def make_markup(request, pk, img_pk, idx):
    nn      = NN.objects.get(pk = pk)
    to_send = json.dumps({"current_idx": idx,
                          "paths": [[img.thumbnail.url, img.trained]
                                    for img in nn.nnimage_set.all().order_by('trained')]})
    context = {"nn": nn,
               "json_arg": to_send}
    return render(request, 'image_processing/make_markup.html', context)


@login_required
def upload_files(request, pk):
    nn      = NN.objects.get(pk = pk)
    context = {"nn": nn}
    return render(request, 'image_processing/upload_files.html', context)


@login_required
def check(request, pk):
    if request.method == "POST":
        uploaded_contents = request.FILES['file'].read()
        nn                = NN.objects.get(pk = pk)
        print(request.FILES['file'])
        print(request.FILES.getlist('files'))
        context           = {"nn": nn,
                             "single_file": request.FILES['file'],
                             "multiple_files": ", ".join(str(fl) for fl in request.FILES.getlist('files'))}
        # return render(request, 'image_processing/test.html', context)
        # return HttpResponse(request, 'hehe')
        # return HttpResponseRedirect('/floppa/')   # works
        return render(request, 'image_processing/test_nn.html', context)
    else:
        return HttpResponse(request, '<h3>not implemented yet</h3>')


@login_required
def nn(request):
    NNs = NN.objects.all()
    context = {'NNs': NNs}
    return render(request, 'image_processing/NN.html', context)
