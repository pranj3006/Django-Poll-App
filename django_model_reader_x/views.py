from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django_model_reader_x.services.django_model_reader_service import \
    DjangoModelReaderService as ModelReaderService

# Create your views here.

def get_models_data(request):
    serv_mdreader = ModelReaderService()
    schema_data = serv_mdreader.get_all_models_data()
    
    return JsonResponse(schema_data,status=200)

def view_models_list(request):
    serv_mdreader = ModelReaderService()
    schema_data = serv_mdreader.get_all_models_data()
    context = {
        'title': 'Database Tables List',
        'schema_data': schema_data,
    }
    return render(request, 'table_view.html', context)

def view_models_scehma(request):
    serv_mdreader = ModelReaderService()
    schema_data = serv_mdreader.get_all_models_data()
    context = {
        'title': 'Database Schema Visualization',
        'schema_data': schema_data,
    }
    return render(request, 'gojs_schema_visualization.html', context)
