from django.db import models

class GreenhouseData(models.Model):
    """
    Model to store greenhouse data.
    """
    id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=255, null=False, blank=False)
    category = models.CharField(max_length=255, null=True, blank=True)
    metric = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField()
    value = models.FloatField(null=True, blank=True)
    subcategory = models.CharField(max_length=255, null=True, blank=True)

