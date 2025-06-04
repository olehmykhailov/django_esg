from django.db import models

class Metadata(models.Model):
    """
    Model to store metadata for environmental reports.
    """
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255, null=True, blank=True)
    metric = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255)
    year = models.IntegerField()
    value = models.FloatField(null=True, blank=True)



