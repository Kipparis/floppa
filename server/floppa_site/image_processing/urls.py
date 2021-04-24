from django.urls import path

from . import views

app_name = 'image_processing'
urlpatterns = [
    path('',            views.nn_select, name='index'),
    path('nns/',        views.nn_select, name='nn_select'),

    path('nn/<int:pk>/',views.nn_detail, name='nn_detail'),
    path('nn/images_preview/<int:pk>/',
         views.nn_images_preview,
         name='nn_images_preview'),
    path('nn/add_category/<int:pk>/',
         views.nn_add_category,
         name='nn_add_category'),
]
