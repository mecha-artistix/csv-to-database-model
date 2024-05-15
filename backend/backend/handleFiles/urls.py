from django.urls import path, include
from .views import *
urlpatterns = [
    path('receive-data/', receive_data, name='receive-data'),
    path('csv/', include('handleFiles.file_storage.urls'))
]