from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from .models import Rawdata
import os
import re
# from .file_storage.views import *
'''
file_names = ['file1.txt', 'file2.txt', 'file3.txt']
data = ['Data for file1', 'Data for file2', 'Data for file3']

# Open multiple files using a context manager
with open(file_names[0], 'w') as file1, open(file_names[1], 'w') as file2, open(file_names[2], 'w') as file3:
    file1.write(data[0])
    file2.write(data[1])
    file3.write(data[2])

'''


current_script_path = os.path.abspath(__file__)
app_directory = os.path.dirname(current_script_path)
file_storage_path = os.path.join(app_directory, 'file_storage')
file_model = os.path.join(file_storage_path, 'models.py')
file_serializer = os.path.join(file_storage_path, 'serializers.py')
file_view = os.path.join(file_storage_path, 'views.py')
file_url = os.path.join(file_storage_path, 'urls.py')

with open(file_model, 'w') as model, open(file_serializer, 'w') as serializer, open(file_view, 'w') as view, open(file_url, 'w') as view:
    model.write('from django.db import models'+'\n')
    serializer.write('from rest_framework import serializers'+'\n')
    view.write('from')

dump = os.path.join(file_storage_path, 'dump.txt')

# Create your views here.
logger = logging.getLogger(__name__)


@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        # Decode the request body and parse JSON
        data = json.loads(request.body.decode('utf-8'))
        file_name = data['fileName']
        file_content = data['fileContent']
        # Check if content already exists in the table
        if Rawdata.objects.filter(file_content=file_content).exists():
            return JsonResponse({"status": "error", "message": "File content already exists."}, status=400)
        
        # Create a new RawData object and save it
        raw_data_entry = Rawdata(file_content=file_content, file_name=file_name)
        raw_data_entry.save()
        return JsonResponse({"status": "success", "message": "Data received and saved."}, status=200)
    elif request.method == 'GET':
        # Convert data to a list of strings to be JSON serializable
        data_list = Rawdata.objects.all().values("file_name", "file_content")
        return JsonResponse({"status": "success", "data": list(data_list)}, status=200)
    else:
        return HttpResponse("Method not allowed", status=405)



# Fetch all RawData instances from the database
all_raw_data = Rawdata.objects.all().values("file_name", "file_content")
def convert_string(value):
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    return value


def determine_field_type(value):
    try:
        int(value)
        return 'IntegerField()'
    except ValueError:
        pass
    try:
        float(value)
        return 'FloatField()'
    except ValueError:
        pass
    if value.lower() == 'true' or value.lower() == 'false':
        return 'BooleanField()'
    if re.match(r'\d{4}-\d{2}-\d{2}', value):
        return 'DateField()'
    return 'CharField(max_length=250)'


with open(dump, 'w') as dump:
    with open(file_model, 'w') as model, open(file_serializer, 'w') as serializer, open(file_view, 'w') as view, open(file_url, 'w') as urls:
        model.write('from django.db import models')
        model.write('\n'*3)
        serializer.write('from rest_framework import serializers'+'\n'+'from .models import *'+'\n')
        serializer.write('\n'*3)
        view.write('''from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response''')
        view.write('\n'*3)

        urls.write('''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()'''+ '\n'*3)
        

        i = 0
        while (i < len(all_raw_data)):
            entry = all_raw_data[i]
            # json.dump(entry, dump)
            name = entry['file_name'].split('.')[0]
            body = entry['file_content']
            body = re.sub(r'\n\s*\n', '\n', body)
            dump.write(name + '\n')
            for line in  body.split('\n'):
                dump.write(line + '\n')
            keys =[re.sub(r'[\[#.*?\.0-9\]]', '', key) for key in  body.split('\n')[0].split(',')]
            row1 = body.split('\n')[1].split(',')

            types = []
            # values = []
            
            print('row1-', row1)
            for item in row1:
                types.append(determine_field_type(item))
            fields = dict(zip(keys, types))
            print(fields)
            model.write(f'class {name}(models.Model):'+ '\n')
            json.dump(fields, dump)
            return_str = ''
            for key, value in fields.items():
                model.write('\t' +f'{key} = models.{value}' +'\n')

            model.write('\n') 
            model.write('\t'+ 'def __str__(self):'+'\n\t\t')
            return_kw = list(fields.keys())[0]
            model.write( f"return self.{list(fields.keys())[0]}")
            model.write('\n\n\n')

            # WRITE SERIALIZER --------
            serializer.write('\n'+f"class {name}Serializer(serializers.ModelSerializer):"+'\n')
            serializer.write('\tclass Meta:'+'\n')
            serializer.write(f'\t\tmodel = {name}'+'\n')
            serializer.write(f"\t\tfields = '__all__'"+'\n')
            serializer.write(f"\t\textra_kwargs = {{field: {{'allow_null': True, 'required': False}} for field in fields}}")

            # WRITE VIEWS ------
            view.write(f"class {name}ViewSet(viewsets.ModelViewSet):"+'\n')
            view.write('\t'+f"queryset = {name}.objects.all()"+'\n')
            view.write('\t'+f"serializer_class = {name}Serializer" +'\n'*3)


            # WRITE PATTERNS ------
            urls.write(f"router.register(r'{name}', {name}ViewSet)"+'\n')
            
            i = i + 1
            print("---"*10)
        urls.write('\n'+f"urlpatterns = [path('file/', include(router.urls))]")


