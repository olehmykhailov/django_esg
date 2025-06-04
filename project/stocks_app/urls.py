from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('charts/', views.ticker_list, name='ticker_list'),
    path('charts/<str:ticker>/', views.stock_chart, name='stock_chart'),
    path('upload/stocks/', views.upload_stocks, name='upload_stocks'),
    
    # API endpoints
    path('api/predict/', views.save_predict, name='save_predict'),
    path('api/predict/batch/', views.save_predict_batch, name='save_predict_batch'),
    path('api/chart-data/<str:ticker>/', views.get_chart_data, name='get_chart_data'),
    path('api/real-data/', views.get_real_data, name='get_real_data'),
    path('api/all-data/', views.get_all_tickers_data, name='get_all_tickers_data'),
    path('api/latest/<str:ticker>/', views.get_ticker_latest, name='get_ticker_latest'),
]
