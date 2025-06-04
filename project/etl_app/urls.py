from django.urls import path
from . import views

urlpatterns = [
    path('greenhouse/', views.upload_greenhouse, name='upload_greenhouse'),
    path('energy/', views.upload_energy, name='upload_energy'),
    path('metadata/', views.upload_metadata, name='upload_metadata'),
    path('diversity/', views.upload_diversity, name='upload_diversity'),
]
