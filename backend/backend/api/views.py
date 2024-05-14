from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
# Create your views here.


def simple_api(request):
    data = {
        "message": "Hello from Django!",
        "items": ["Item 1", "Item 2", "Item 3"],
    }
    return JsonResponse(data)


