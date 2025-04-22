"""
URL configuration for kindred_causes main app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('browse_events/', views.event_browser.as_view(), name='event_browser'),
    
    path('notification/new/', views.NotificationCreateView.as_view(), name='new_notification'),
    path('inbox/', views.NotificationInboxView.as_view(), name='inbox'),
    path('inbox/view/<int:pk>/', views.NotificationDetailView.as_view(), name='view_notification'),
    
    path('account/', views.AccountView.as_view(), name='account'),
    path('volunteer_history/', views.TaskHistoryView.as_view(), name='volunteer_history'),
    path('matching_form/', views.matching_form, name='matching_form'),

    path('join_event/<int:event_id>', views.JoinEventView.as_view(), name='join_event'),
    path('leave_event/<int:event_id>', views.LeaveEventView.as_view(), name='leave_event'),

    path('assign_user_to_task/<int:user_id>/<int:task_id>', views.AssignTaskView.as_view(), name='assign_user_to_task'),
    path('remove_user_from_task/<int:user_id>/<int:task_id>', views.RemoveTaskView.as_view(), name='remove_user_from_task'),
    

    path('', views.LandingView.as_view(), name='landing'),
    path('home/', views.HomeView.as_view(), name='home'),

    path('event/new/', views.EventCreateView.as_view(), name='new_event'),
    path('event/view/<int:pk>/', views.EventDetailView.as_view(), name='view_event'),
    path('event/edit/<int:pk>/', views.EventUpdateView.as_view(), name='edit_event'),
    path('event/delete/<int:pk>/', views.EventDeleteView.as_view(), name='delete_event'),
    path('event/<int:pk>/report-pdf/', views.generate_event_report_pdf, name='generate_event_report_pdf'),
    path('event/<int:pk>/report-csv/', views.export_event_report_csv, name='generate_event_report_csv'),

    path('task/new/<int:event_id>', views.TaskCreateView.as_view(), name='new_task'),
    path('task/view/<int:pk>/', views.TaskDetailView.as_view(), name='view_task'),
    path('task/edit/<int:pk>', views.TaskUpdateView.as_view(), name='edit_task'),
    path('task/delete/<int:pk>/', views.TaskDeleteView.as_view(), name='delete_task'),
    
        
    path('account_management/', views.AccountManagementView.as_view(), name='account_management'),    
    path('event-review/edit/<int:pk>/', views.EventReviewUpdateView.as_view(), name='edit_event_review'),
    path("event/<int:event_pk>/review/new/", views.EventReviewCreateView.as_view(), name="new_event_review"),

    path('skill-management/', views.SkillManagementCreateView.as_view(), name="new_skill_management"),
    path('skill-management/edit/<int:pk>/', views.SkillManagementUpdateView.as_view(), name='edit_skill_management'),
    path('browse_skills/', views.skill_browser, name='skill_browser'),
]
