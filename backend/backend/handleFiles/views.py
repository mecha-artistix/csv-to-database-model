from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from .models import Rawdata
import os
# print(os.getcwd())
current_script_path = os.path.abspath(__file__)
app_directory = os.path.dirname(current_script_path)
file_storage_path = os.path.join(app_directory, 'file_storage')
file_path = os.path.join(file_storage_path, 'received_data.txt')
# print(file_path)



# Create your views here.
logger = logging.getLogger(__name__)


@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        # Decode the request body and parse JSON
        data = json.loads(request.body.decode('utf-8'))
        file_name = data['fileName']
        file_content = data['fileContent']
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



with open(file_path, 'w') as file:
    for entry in all_raw_data:
        
        name = entry['file_name'].split('.')[0]
        body = entry['file_content']
        rows = body.split('\n')
        keys = body.split('\n')[0].split(',')
        types = []
        for item in rows[1].split(','):
            types.append(type(item).__name__)
        file.write(f'class {name}(models.Model):'+ '\n')
        for key in keys:
            file.write('\t' +f'{key} = models.CharField(max_length=250)' +'\n')
        file.write('\n') 
        file.write('\t'+ 'def __str__(self):'+'\n\t\t')
        file.write( f'return' )
        file.write('\n\n\n')
        print(name)


# return f"Rate ID {self.id}: {self.rate} per {self.rate_unit}"
