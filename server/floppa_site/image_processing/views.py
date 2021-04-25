import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from django.conf import settings

from .models import Category,NN,NNImage,Category,NNImageMarkup

from pathlib import Path


@login_required
def nn_select(request):
    if request.method == "POST":
        nn = NN.create_new(request.POST['nn_name'],
                           settings.BASE_DIR/Path("images/floppa_in_bath.jpg"))
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
               .values('nnimagemarkup__category__name')
               .filter(nn = nn)
               .annotate(total=Count("id"))
               .filter(nnimagemarkup__category__name__isnull=False, total__lt=100))
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
               "json_arg": to_send,
               "img_pk": img_pk,
               "idx": idx}

    if request.method == "POST":
        context["inc_json"] = request.POST['json_inc']
        json_string = request.POST['json_inc']
        inc_dict = json.loads(json_string)
        for key, val in inc_dict.items():
            name = Path(key).name
            print("nameeeeee:", name)
            image = NNImage.objects.get(name = Path(key).stem.replace("_", " "))
            if image.trained:
                continue
            for defect in val:
                cat = Category.objects.get(name = defect['tag'])
                defect_coords = NNImageMarkup(image = image,
                                              x1 = defect['x1'],
                                              x2 = defect['x2'],
                                              y1 = defect['y1'],
                                              y2 = defect['y2'],
                                              category = cat)
                defect_coords.save()
            image.trained = True
            image.save()

    return render(request, 'image_processing/make_markup.html', context)


@login_required
def upload_files(request, pk):
    nn      = NN.objects.get(pk = pk)
    context = {"nn": nn}
    return render(request, 'image_processing/upload_files.html', context)


@login_required
def check(request, pk):
    if request.method == "POST":
        nn                = NN.objects.get(pk = pk)
        # add images to existing
        files = request.FILES.getlist('files')
        print(request.FILES.getlist('files'))
        for fl in files:
            print(fl.name)
            image = NNImage(name = fl.name, thumbnail = fl, nn=nn, trained=False)
            image.save()
        num_in_rows = 7
        images = []
        for i, image in enumerate(nn.nnimage_set.all().order_by('trained')):
            if (i % num_in_rows) == 0: images.append([])
            images[-1].append(image)
        context = {"nn": nn, "images": images}
        return render(request, 'image_processing/nn_images_preview.html', context)
    else:
        return HttpResponse(request, '<h3>not implemented yet</h3>')


@login_required
def apply_nn(request, pk):
    if request.method == "POST":
        nn            = NN.objects.get(pk = pk)
        files = request.FILES.getlist('files')
        print(request.FILES.getlist('files'))
        for fl in files:
            print(fl.name)
        # ret = func()
        context = {"nn": nn,"files": [fl.name for fl in files]}
        return render(request, 'image_processing/nn_output.html', context)
    else:
        return HttpResponse(request, "use post")


@login_required
def nn(request):
    NNs = NN.objects.all()
    context = {'NNs': NNs}
    return render(request, 'image_processing/NN.html', context)
