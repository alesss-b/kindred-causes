"""
URL configuration for kindred_causes main app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.user_registration, name='user_registration'),
    # path('login/', views.login, name='login'),
    path('browse_events/', views.event_browser, name='event_browser'),
    path('preview_event/', views.event_preview, name='event_preview'),
    path('home/', views.home, name='home'),
    path('inbox/', views.inbox, name='inbox'),
    path('account/', views.account, name='account'),
    path('volunteer_history/', views.volunteer_history, name='volunteer_history'),
    path('matching_form/', views.matching_form, name='matching_form'),

    path('event-management/new/', views.EventManagementCreateView.as_view(), name='new_event_management'),
    path('event-management/edit/<int:pk>/', views.EventManagementUpdateView.as_view(), name='edit_event_management'),
    
    path('account_management/', views.account_management, name='account_management'),
    path('event-review/edit/<int:pk>/', views.EventReviewUpdateView.as_view(), name='edit_event_review'),
    path('event-review/new/', views.EventReviewCreateView.as_view(), name='new_event_review'),
]
