from django.db import models

# Create your models here.



class Rate(models.Model):
    connect_fee = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    rate_unit = models.CharField(max_length=50)
    rate_increment = models.IntegerField()
    group_interval_start = models.IntegerField()

    def __str__(self):
        return f"Rate ID {self.id}: {self.rate} per {self.rate_unit}"
