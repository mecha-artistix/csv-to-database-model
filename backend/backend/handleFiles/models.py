from django.db import models
from .file_storage.models import *
# Create your models here.

class Rawdata(models.Model):
    file_content = models.TextField()
    file_name = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.file_name}: {self.file_content[:50]}"