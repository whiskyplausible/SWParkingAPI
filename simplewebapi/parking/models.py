from django.db import models
from django.contrib.postgres.fields import JSONField

class CarParks(models.Model):
    carpark_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=9, blank=True)
    location = models.CharField(max_length=32, blank=True)
    spaces = models.PositiveIntegerField(blank=True)
    min_cost_pence = models.PositiveIntegerField(blank=True)
    features = JSONField()
    operator = models.CharField(max_length=60, blank=True)
