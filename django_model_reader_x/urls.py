from django.contrib import admin
from django.urls import path, include
from . import views
app_name='django_model_reader_x'
urlpatterns = [
    path('view_models_list/', views.view_models_list, name='view_models_list'),
    path('view_models_scehma/', views.view_models_scehma, name='view_models_scehma'),
    path('get_models_data/', views.get_models_data, name='get_models_data'),
]
