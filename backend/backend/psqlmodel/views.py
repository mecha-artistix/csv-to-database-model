from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize
from .models import Rate
import json
import logging
# Create your views here.

def psqlapi(request):
    data = {
        "message": "Hello from PSQL!",
        "items": ["Item 1", "Item 2", "Item 3"],
    }
    return JsonResponse(data)



# Create your views here.

@csrf_exempt  # Disable CSRF token for simplicity in testing; not recommended for production
@require_http_methods(["POST"])  # Allow only POST requests
def create_rate(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        # Check if a rate with the exact same data already exists
        if Rate.objects.filter(
            connect_fee=data['connect_fee'],
            rate=data['rate'],
            rate_unit=data['rate_unit'],
            rate_increment=data['rate_increment'],
            group_interval_start=data['group_interval_start']
        ).exists():
            return JsonResponse({'message': 'No changes detected, record not added.'}, status=200)

        # If no existing rate matches the input, create a new rate
        rate = Rate.objects.create(
            connect_fee=data['connect_fee'],
            rate=data['rate'],
            rate_unit=data['rate_unit'],
            rate_increment=data['rate_increment'],
            group_interval_start=data['group_interval_start']
        )
        return JsonResponse({'message': 'Rate created successfully', 'id': rate.id}, status=201)
    except (KeyError, TypeError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)



@csrf_exempt
@require_http_methods(["GET"])
def get_rates(request):
    # Fetch all rate records from the database
    # rates = Rate.objects.all().values(
    #     'connect_fee', 'rate', 'rate_unit', 'rate_increment', 'group_interval_start'
    # )   
    # rates_list = list(rates_serialized)  # Convert QuerySet to list of dicts
    # all data types sent were strings
    rates = Rate.objects.all()
    rates_serialized = serialize('json', rates, fields=('connect_fee', 'rate', 'rate_unit', 'rate_increment', 'group_interval_start'))
    return HttpResponse(rates_serialized,  content_type="application/json")



