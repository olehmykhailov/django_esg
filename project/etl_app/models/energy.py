from django.db import models

# Category,Subcategory,Metric,Unit,Year,Value
# Corporate facilities energy use,Electricity,U.S.,MWh,2021,2377000.0

class EnergyData(models.Model):
    """
    Model to store energy data.
    """
    id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)
    metric = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    year = models.IntegerField()
    value = models.FloatField(null=True, blank=True)

