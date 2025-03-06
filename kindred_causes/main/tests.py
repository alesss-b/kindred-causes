from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.utils import timezone
from django.contrib.messages.storage.fallback import FallbackStorage
from datetime import datetime, timedelta

from .models import Skill, Event, Task, Notification, AttendeeReview, EventReview
from .forms import EventReviewForm, EventManagementForm
from .views import (HomeView, LandingView, EventReviewCreateView, EventReviewUpdateView,
                  EventManagementCreateView, EventManagementUpdateView, event_browser,
                  event_preview, event_management, user_registration, volunteer_history,
                  matching_form, inbox, account, account_management)
from .choices import EventStatus, EventUrgency

# Create your tests here.
class ChoicesTestCase(TestCase):
    """Test cases for choices module"""
    
    def test_event_status_choices(self):
        """Test EventStatus choices are defined correctly"""
        self.assertEqual(EventStatus.NOT_STARTED, "Not Started")
        self.assertEqual(EventStatus.IN_PROGRESS, "In Progress")
        self.assertEqual(EventStatus.COMPLETED, "Completed")
        
    def test_event_urgency_choices(self):
        """Test EventUrgency choices are defined correctly"""
        self.assertEqual(EventUrgency.CRITICAL, 4)
        self.assertEqual(EventUrgency.HIGH, 3)
        self.assertEqual(EventUrgency.MEDIUM, 2)
        self.assertEqual(EventUrgency.LOW, 1)


class ModelTestCase(TestCase):
    """Test cases for models"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        self.skill = Skill.objects.create(
            name='Test Skill',
            description='Test Skill Description',
            created_by=self.user,
            updated_by=self.user
        )
        
        self.event = Event.objects.create(
            name='Test Event',
            description='Test Event Description',
            location='Test Location',
            urgency=EventUrgency.MEDIUM,
            date=timezone.now(),
            created_by=self.user,
            updated_by=self.user
        )
        self.event.required_skills.add(self.skill)
        
        self.task = Task.objects.create(
            event=self.event,
            name='Test Task',
            description='Test Task Description',
            capacity=10,
            location='Test Task Location',
            created_by=self.user,
            updated_by=self.user
        )
        
        self.notification = Notification.objects.create(
            event=self.event,
            subject='Test Notification',
            body='Test Notification Body',
            created_by=self.user,
            updated_by=self.user
        )
        
        self.attendee_review = AttendeeReview.objects.create(
            attendee=self.user,
            event=self.event,
            rating=5,
            comments='Test Attendee Review Comments',
            created_by=self.user,
            updated_by=self.user
        )
        
        self.event_review = EventReview.objects.create(
            event=self.event,
            rating=4,
            comments='Test Event Review Comments',
            created_by=self.user,
            updated_by=self.user
        )
    
    def test_skill_model(self):
        """Test Skill model creation"""
        self.assertEqual(str(self.skill), 'Test Skill')
        self.assertEqual(self.skill.description, 'Test Skill Description')
        self.assertEqual(self.skill.created_by, self.user)
        self.assertEqual(self.skill.updated_by, self.user)
    
    def test_event_model(self):
        """Test Event model creation"""
        self.assertEqual(str(self.event), 'Test Event: Test Event Description')
        self.assertEqual(self.event.location, 'Test Location')
        self.assertEqual(self.event.urgency, EventUrgency.MEDIUM)
        self.assertTrue(self.event.required_skills.filter(pk=self.skill.pk).exists())
        self.assertEqual(self.event.created_by, self.user)
        self.assertEqual(self.event.updated_by, self.user)
    
    def test_task_model(self):
        """Test Task model creation"""
        self.assertEqual(str(self.task), 'Test Task')
        self.assertEqual(self.task.event, self.event)
        self.assertEqual(self.task.capacity, 10)
        self.assertEqual(self.task.location, 'Test Task Location')
        self.assertEqual(self.task.created_by, self.user)
        self.assertEqual(self.task.updated_by, self.user)
    
    def test_notification_model(self):
        """Test Notification model creation"""
        self.assertEqual(str(self.notification), 'Test Notification Test Notification Body')
        self.assertEqual(self.notification.event, self.event)
        self.assertEqual(self.notification.subject, 'Test Notification')
        self.assertEqual(self.notification.body, 'Test Notification Body')
        self.assertEqual(self.notification.created_by, self.user)
        self.assertEqual(self.notification.updated_by, self.user)
    
    def test_attendee_review_model(self):
        """Test AttendeeReview model creation"""
        self.assertEqual(self.attendee_review.attendee, self.user)
        self.assertEqual(self.attendee_review.event, self.event)
        self.assertEqual(self.attendee_review.rating, 5)
        self.assertEqual(self.attendee_review.comments, 'Test Attendee Review Comments')
        self.assertEqual(self.attendee_review.created_by, self.user)
        self.assertEqual(self.attendee_review.updated_by, self.user)
    
    def test_event_review_model(self):
        """Test EventReview model creation"""
        self.assertEqual(str(self.event_review), 'Test Event : 4')
        self.assertEqual(self.event_review.event, self.event)
        self.assertEqual(self.event_review.rating, 4)
        self.assertEqual(self.event_review.comments, 'Test Event Review Comments')
        self.assertEqual(self.event_review.created_by, self.user)
        self.assertEqual(self.event_review.updated_by, self.user)


class FormTestCase(TestCase):
    """Test cases for forms"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        self.skill = Skill.objects.create(
            name='Test Skill',
            description='Test Skill Description',
            created_by=self.user,
            updated_by=self.user
        )
        
        self.event = Event.objects.create(
            name='Test Event',
            description='Test Event Description',
            location='Test Location',
            urgency=EventUrgency.MEDIUM,
            date=timezone.now(),
            created_by=self.user,
            updated_by=self.user
        )
        self.event.required_skills.add(self.skill)
    
    def test_event_review_form_valid(self):
        """Test EventReviewForm with valid data"""
        form_data = {
            'event': self.event.id,
            'rating': 5,
            'comments': 'Test Event Review Comments'
        }
        form = EventReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_event_review_form_invalid(self):
        """Test EventReviewForm with invalid data"""
        # Missing required field 'event'
        form_data = {
            'rating': 5,
            'comments': 'Test Event Review Comments'
        }
        form = EventReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('event', form.errors)
        
        # Invalid rating (out of range)
        form_data = {
            'event': self.event.id,
            'rating': 6,
            'comments': 'Test Event Review Comments'
        }
        form = EventReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
    
    def test_event_management_form_valid(self):
        """Test EventManagementForm with valid data"""
        form_data = {
            'name': 'New Test Event',
            'description': 'New Test Event Description',
            'location': 'New Test Location',
            'urgency': EventUrgency.HIGH,
            'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'required_skills': self.skill.id
        }
        form = EventManagementForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_event_management_form_invalid(self):
        """Test EventManagementForm with invalid data"""
        # Missing required field 'name'
        form_data = {
            'description': 'New Test Event Description',
            'location': 'New Test Location',
            'urgency': EventUrgency.HIGH,
            'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'required_skills': self.skill.id
        }
        form = EventManagementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        
        # Invalid urgency value
        form_data = {
            'name': 'New Test Event',
            'description': 'New Test Event Description',
            'location': 'New Test Location',
            'urgency': 10,  # Invalid value
            'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'required_skills': self.skill.id
        }
        form = EventManagementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('urgency', form.errors)


class ViewTestCase(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.factory = RequestFactory()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        self.skill = Skill.objects.create(
            name='Test Skill',
            description='Test Skill Description',
            created_by=self.user,
            updated_by=self.user
        )
        
        self.event = Event.objects.create(
            name='Test Event',
            description='Test Event Description',
            location='Test Location',
            urgency=EventUrgency.MEDIUM,
            date=timezone.now(),
            created_by=self.user,
            updated_by=self.user
        )
        self.event.required_skills.add(self.skill)
        
        self.event_review = EventReview.objects.create(
            event=self.event,
            rating=4,
            comments='Test Event Review Comments',
            created_by=self.user,
            updated_by=self.user
        )
    
    def test_landing_view_authenticated(self):
        """Test LandingView with authenticated user"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertRedirects(response, reverse('home'))
    
    def test_landing_view_unauthenticated(self):
        """Test LandingView with unauthenticated user"""
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')
    
    def test_home_view_authenticated(self):
        """Test HomeView with authenticated user"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_home_view_unauthenticated(self):
        """Test HomeView with unauthenticated user"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/')
    
    def test_event_review_create_view_authenticated(self):
        """Test EventReviewCreateView with authenticated user"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('new_event_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_review_form.html')
        
        # Test POST request
        form_data = {
            'event': self.event.id,
            'rating': 5,
            'comments': 'New Test Event Review Comments'
        }
        response = self.client.post(reverse('new_event_review'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        
        # Verify the review was created
        self.assertTrue(EventReview.objects.filter(comments='New Test Event Review Comments').exists())
    
    def test_event_review_create_view_unauthenticated(self):
        """Test EventReviewCreateView with unauthenticated user"""
        response = self.client.get(reverse('new_event_review'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue('/login/' in response.url)
    
    def test_event_review_update_view_authenticated(self):
        """Test EventReviewUpdateView with authenticated user"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edit_event_review', kwargs={'pk': self.event_review.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_review_form.html')
        
        # Test POST request
        form_data = {
            'event': self.event.id,
            'rating': 3,
            'comments': 'Updated Test Event Review Comments'
        }
        response = self.client.post(reverse('edit_event_review', kwargs={'pk': self.event_review.id}), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        
        # Verify the review was updated
        self.event_review.refresh_from_db()
        self.assertEqual(self.event_review.rating, 3)
        self.assertEqual(self.event_review.comments, 'Updated Test Event Review Comments')
    
    def test_event_review_update_view_unauthenticated(self):
        """Test EventReviewUpdateView with unauthenticated user"""
        response = self.client.get(reverse('edit_event_review', kwargs={'pk': self.event_review.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue('/login/' in response.url)
    
    def test_event_management_create_view(self):
        """Test EventManagementCreateView"""
        response = self.client.get(reverse('new_event_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_management.html')
        
        # Test POST request
        form_data = {
            'name': 'New Managed Event',
            'description': 'New Managed Event Description',
            'location': 'New Managed Location',
            'urgency': EventUrgency.HIGH,
            'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'required_skills': self.skill.id
        }
        response = self.client.post(reverse('new_event_management'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        
        # Verify the event was created
        self.assertTrue(Event.objects.filter(name='New Managed Event').exists())
    
    def test_event_management_update_view(self):
        """Test EventManagementUpdateView"""
        response = self.client.get(reverse('edit_event_management', kwargs={'pk': self.event.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_management.html')
        
        # Test POST request
        form_data = {
            'name': 'Updated Managed Event',
            'description': 'Updated Managed Event Description',
            'location': 'Updated Managed Location',
            'urgency': EventUrgency.LOW,
            'date': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M'),
            'required_skills': self.skill.id
        }
        response = self.client.post(reverse('edit_event_management', kwargs={'pk': self.event.id}), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        
        # Verify the event was updated
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, 'Updated Managed Event')
        self.assertEqual(self.event.description, 'Updated Managed Event Description')
        self.assertEqual(self.event.urgency, EventUrgency.LOW)
    
    def test_function_based_views(self):
        """Test function-based views"""
        # Test event_browser view
        response = self.client.get(reverse('event_browser'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_browser.html')
        self.assertEqual(response.context['test_key'], 'test_value')
        
        # Test event_preview view
        response = self.client.get(reverse('event_preview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_preview.html')
        self.assertEqual(response.context['test_key'], 'test_value')
        
        # Test user_registration view
        response = self.client.get(reverse('user_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_registration.html')
        self.assertEqual(response.context['test_key'], 'test_value')
        
        # Test volunteer_history view
        response = self.client.get(reverse('volunteer_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'volunteer_history.html')
        self.assertEqual(response.context['test_key'], 'test_value')
        
        # Test matching_form view
        response = self.client.get(reverse('matching_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matching_form.html')
        self.assertEqual(response.context['test_key'], 'test_value')
        
        # Test inbox view
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox.html')
        self.assertEqual(response.context['test_key'], 'test_value')
    
    def test_account_view(self):
        """Test account view"""
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')
        
        # Test default context values
        self.assertEqual(response.context['name'], 'John Doe')
        self.assertEqual(response.context['city'], 'New York')
        self.assertEqual(response.context['state'], 'NY')
        self.assertEqual(response.context['email'], 'john.doe@example.com')
        self.assertEqual(response.context['phone'], '(123) 456-7890')
    
    def test_account_management_view(self):
        """Test account_management view"""
        # Test GET request
        response = self.client.get(reverse('account_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_management.html')
        
        # Test POST request
        form_data = {
            'name': 'Jane Smith',
            'city': 'Chicago',
            'state': 'IL',
            'start_availability': 'January 1, 2020',
            'end_availability': 'December 31, 2025',
            'skills': ['Coding', 'Design'],
            'email': 'jane.smith@example.com',
            'address1': '456 Oak St',
            'address2': 'Apt 789',
            'zipcode': '60601',
            'phone': '(987) 654-3210'
        }
        response = self.client.post(reverse('account_management'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertRedirects(response, reverse('account'))
        
        # Verify session values were updated
        session = self.client.session
        self.assertEqual(session['name'], 'Jane Smith')
        self.assertEqual(session['city'], 'Chicago')
        self.assertEqual(session['state'], 'IL')
        self.assertEqual(session['email'], 'jane.smith@example.com')
        self.assertEqual(session['phone'], '(987) 654-3210')
        self.assertEqual(session['skills'], ['Coding', 'Design'])


class UrlPatternTestCase(TestCase):
    """Test cases for URL patterns"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        self.event = Event.objects.create(
            name='Test Event',
            description='Test Event Description',
            location='Test Location',
            urgency=EventUrgency.MEDIUM,
            date=timezone.now(),
            created_by=self.user,
            updated_by=self.user
        )
        
        self.event_review = EventReview.objects.create(
            event=self.event,
            rating=4,
            comments='Test Event Review Comments',
            created_by=self.user,
            updated_by=self.user
        )
    
    def test_url_patterns(self):
        """Test URL patterns resolve to correct views"""
        # Test function-based view URLs
        self.assertEqual(reverse('user_registration'), '/register/')
        self.assertEqual(reverse('event_browser'), '/browse_events/')
        self.assertEqual(reverse('event_preview'), '/preview_event/')
        self.assertEqual(reverse('inbox'), '/inbox/')
        self.assertEqual(reverse('account'), '/account/')
        self.assertEqual(reverse('volunteer_history'), '/volunteer_history/')
        self.assertEqual(reverse('matching_form'), '/matching_form/')
        self.assertEqual(reverse('landing'), '/')
        self.assertEqual(reverse('home'), '/home/')
        self.assertEqual(reverse('account_management'), '/account_management/')
        
        # Test class-based view URLs
        self.assertEqual(reverse('new_event_management'), '/event-management/new/')
        self.assertEqual(reverse('edit_event_management', kwargs={'pk': self.event.id}),
                         f'/event-management/edit/{self.event.id}/')
        self.assertEqual(reverse('edit_event_review', kwargs={'pk': self.event_review.id}),
                         f'/event-review/edit/{self.event_review.id}/')
        self.assertEqual(reverse('new_event_review'), '/event-review/new/')

#required dont know
class IntegrationTestCase(TestCase):
    """Integration tests for the application"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        self.skill = Skill.objects.create(
            name='Test Skill',
            description='Test Skill Description',
            created_by=self.user,
            updated_by=self.user
        )
    
    def test_event_creation_to_review_flow(self):
        """Test complete flow from event creation to reviewing"""
        self.client.login(username='testuser', password='testpassword')
        
        # 1. Create an event
        event_data = {
            'name': 'Integration Test Event',
            'description': 'Integration Test Event Description',
            'location': 'Integration Test Location',
            'urgency': EventUrgency.HIGH,
            'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'required_skills': self.skill.id
        }
        response = self.client.post(reverse('new_event_management'), event_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        
        # Verify the event was created
        event = Event.objects.get(name='Integration Test Event')
        self.assertEqual(event.description, 'Integration Test Event Description')
        self.assertEqual(event.urgency, EventUrgency.HIGH)
        
        # 2. Create a review for the event
        review_data = {
            'event': event.id,
            'rating': 5,
            'comments': 'Integration Test Event Review'
        }
        response = self.client.post(reverse('new_event_review'), review_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        
        # Verify the review was created
        review = EventReview.objects.get(comments='Integration Test Event Review')
        self.assertEqual(review.event, event)
        self.assertEqual(review.rating, 5)
        
        # 3. Update the event
        update_event_data = {
            'name': 'Updated Integration Test Event',
            'description': 'Updated Integration Test Event Description',
            'location': 'Updated Integration Test Location',
            'urgency': EventUrgency.CRITICAL,
            'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'required_skills': self.skill.id
        }
        response = self.client.post(reverse('edit_event_management', kwargs={'pk': event.id}), update_event_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        
        # Verify the event was updated
        event.refresh_from_db()
        self.assertEqual(event.name, 'Updated Integration Test Event')
        self.assertEqual(event.description, 'Updated Integration Test Event Description')
        self.assertEqual(event.urgency, EventUrgency.CRITICAL)
        
        # 4. Update the review
        update_review_data = {
            'event': event.id,
            'rating': 3,
            'comments': 'Updated Integration Test Event Review'
        }
        response = self.client.post(reverse('edit_event_review', kwargs={'pk': review.id}), update_review_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        
        # Verify the review was updated
        review.refresh_from_db()
        self.assertEqual(review.comments, 'Updated Integration Test Event Review')
        self.assertEqual(review.rating, 3)