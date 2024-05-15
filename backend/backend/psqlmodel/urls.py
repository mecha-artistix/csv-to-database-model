from django.urls import path
from .views import psqlapi, create_rate, get_rates

urlpatterns = [
    path('psql/', psqlapi, name='psql-api'),
    path('create-rate/', create_rate, name='create-rate'),
    path('get-rate/', get_rates, name = 'get-rate'),
    

]
