from django.db import models

#Year,Women in Workforce (%),Black Employees in US (%),Latino Employees in US (%),Asian Employees in US (%),Multiracial Employees in US (%)

class DiversityData(models.Model):
    company = models.CharField(max_length=255)
    year = models.IntegerField()
    women_in_workforce = models.FloatField()
    black_employees = models.FloatField()
    latino_employees = models.FloatField()
    asian_employees = models.FloatField()
    multiracial_employees = models.FloatField()