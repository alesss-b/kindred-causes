"""
URL configuration for kindred_causes main app.
"""
from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.user_registration, name='user_registration'),
    path('browse_events/', views.event_browser, name='event_browser'),
    path('preview_event/', views.event_preview, name='event_preview'),
    
    path('inbox/', views.inbox, name='inbox'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('volunteer_history/', views.volunteer_history, name='volunteer_history'),
    path('matching_form/', views.matching_form, name='matching_form'),

    path('', views.LandingView.as_view(), name='landing'),
    path('home/', views.HomeView.as_view(), name='home'),

    path('event-management/new/', views.EventManagementCreateView.as_view(), name='new_event_management'),
    path('event-management/edit/<int:pk>/', views.EventManagementUpdateView.as_view(), name='edit_event_management'),
    
    path('account_management/', views.AccountManagementView.as_view(), name='account_management'),    
    path('event-review/edit/<int:pk>/', views.EventReviewUpdateView.as_view(), name='edit_event_review'),
    path('event-review/new/', views.EventReviewCreateView.as_view(), name='new_event_review'),
]
