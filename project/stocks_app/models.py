from django.db import models

class StocksData(models.Model):
    """
    Model to store stock data.
    """
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    open = models.FloatField()  # Open price
    high = models.FloatField()  # High price
    low = models.FloatField()  # Low price
    close = models.FloatField()  # Close price
    adj_close = models.FloatField(null=True, blank=True)  # Adjusted close price
    volume = models.BigIntegerField(null=True, blank=True)  # Volume of shares traded
    dividend = models.FloatField(null=True, blank=True)  # Dividend amount
    split = models.FloatField(null=True, blank=True)  # Stock split factor
    

# ticker,company_name,date,o,h,l,c,pc,d,dp
# AAPL,Apple Inc,2020-05-11,77.025,79.2625,76.81,78.7525,,,

class Predict(models.Model):
    """
    Model to store prediction data.
    """
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10)
    close = models.FloatField()  
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('ticker', 'date')  
