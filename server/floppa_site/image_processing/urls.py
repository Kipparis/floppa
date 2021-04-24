from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'image_processing'
urlpatterns = [
    path('',            views.category_select,                name='index'),
    path('categories/', views.category_select,                name='category_select'),
    path('<int:pk>/',   views.category,                       name='category'),
    path('nn/',         views.nn,                             name='nn'),
]
