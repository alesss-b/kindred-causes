"""
URL configuration for kindred_causes main app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
]
