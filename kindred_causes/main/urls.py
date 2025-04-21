"""
URL configuration for kindred_causes main app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('browse_events/', views.event_browser.as_view(), name='event_browser'),
    path('preview_event/', views.event_preview, name='event_preview'),
    
    path('inbox/', views.inbox, name='inbox'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('volunteer_history/', views.TaskHistoryView.as_view(), name='volunteer_history'),
    path('matching_form/', views.matching_form, name='matching_form'),

    path('', views.LandingView.as_view(), name='landing'),
    path('home/', views.HomeView.as_view(), name='home'),

    path('event-management/new/', views.EventManagementCreateView.as_view(), name='new_event_management'),
    path('event-management/edit/<int:pk>/', views.EventManagementUpdateView.as_view(), name='edit_event_management'),
    path('event/view/<int:pk>/', views.EventDetailView.as_view(), name='view_event'),

    path('task/new/<int:event_id>', views.TaskCreateView.as_view(), name='new_task'),
    path('task/view/<int:pk>/', views.TaskDetailView.as_view(), name='view_task'),
        
    path('account_management/', views.AccountManagementView.as_view(), name='account_management'),    
    path('event-review/edit/<int:pk>/', views.EventReviewUpdateView.as_view(), name='edit_event_review'),
    path('event-review/new/', views.EventReviewCreateView.as_view(), name='new_event_review'),

    path('skill-management/', views.SkillManagementCreateView.as_view(), name="new_skill_management"),
    path('skill-management/edit/<int:pk>/', views.SkillManagementUpdateView.as_view(), name='edit_skill_management'),
    path('browse_skills/', views.skill_browser, name='skill_browser'),
    
]
