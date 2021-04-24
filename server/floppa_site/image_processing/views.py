from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Category
from .models import NN

@login_required
def category_select(request):
    categories = Category.objects.all()
    context    = {'categories': categories}
    return render(request, 'image_processing/category_select.html', context)

@login_required
def category(request, pk):
    return HttpResponse(f"yes {pk}")

@login_required
def nn(request):
    NNs = NN.objects.all()
    context = {'NNs': NNs}
    return render(request, 'image_processing/NN.html', context)
