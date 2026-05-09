from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rizdvo/', views.rizdvo, name='rizdvo'),
    path('obzhynky/', views.obzhynky, name='obzhynky'),
    path('kupala/', views.kupala, name='kupala'),
    path('velykden/', views.velykden, name='velykden'),
    path('pobut/', views.pobut, name='pobut'),
]