"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from etl_app import views as etl_views
from stocks_app import views as stocks_views

urlpatterns = [
    path('upload/greenhouse/', etl_views.upload_greenhouse, name='upload_greenhouse'),
    path('upload/energy/', etl_views.upload_energy, name='upload_energy'),
    path('upload/metadata/', etl_views.upload_metadata, name='upload_metadata'),
    path('upload/diversity/', etl_views.upload_diversity, name='upload_diversity'),
    path('upload/stocks/', stocks_views.upload_stocks, name='upload_stocks'),
    
    # API endpoints
    path('api/predict/', stocks_views.save_predict, name='save_predict'),
    path('api/real-data/', stocks_views.get_real_data, name='get_real_data'),
]

