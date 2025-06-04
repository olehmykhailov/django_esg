from django.db import models

class StocksData(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    adj_close = models.FloatField(null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    dividend = models.FloatField(null=True, blank=True)
    split = models.FloatField(null=True, blank=True)
    

class Predict(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10)
    close = models.FloatField()  
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('ticker', 'date')
