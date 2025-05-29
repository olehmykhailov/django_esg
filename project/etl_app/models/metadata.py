from django.db import models

class Metadata(models.Model):
    """
    Model to store metadata for environmental reports.
    """
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    year = models.IntegerField()
    date_of_publication = models.DateField()
    source = models.CharField(max_length=255)
    link = models.URLField()



