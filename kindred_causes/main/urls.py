"""
URL configuration for kindred_causes main app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.user_registration, name='user_registration'),
    path('login/', views.login, name='login'),
    path('browse_events/', views.event_browser, name='event_browser'),
    path('preview_event/', views.event_preview, name='event_preview'),
    path('home/', views.home, name='home'),
    path('inbox/', views.inbox, name='inbox'),
    path('account/', views.account, name='account'),
]
