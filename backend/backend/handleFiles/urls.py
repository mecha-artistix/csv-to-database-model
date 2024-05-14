from django.urls import path
from .views import *
urlpatterns = [
    path('receive-data/', receive_data, name='receive-data'),
]