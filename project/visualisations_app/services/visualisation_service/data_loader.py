import pandas as pd
from django.conf import settings
from stocks_app.models import StocksData, Predict
from etl_app.models import GreenhouseData, EnergyData, Metadata, DiversityData

def load_stock_df():
    data = StocksData.objects.all().values('date', 'close')
    df = pd.DataFrame(data)

    return df

def load_ghg_df():
    data = GreenhouseData.objects.all()
    df = pd.DataFrame(data)
    return df

def load_diversity_df():
    data = DiversityData.objects.all()
    df = pd.DataFrame(data)

    return df

def load_energy_df():
    data = EnergyData.objects.all()
    df = pd.DataFrame(data)

    return df