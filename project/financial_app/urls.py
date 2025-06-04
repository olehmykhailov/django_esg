from django.urls import path
from . import views

urlpatterns = [
    path('financial/', views.upload_financial_data, name='upload_financial_data'),
]
