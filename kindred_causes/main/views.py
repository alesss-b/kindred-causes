from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView
from .models import AvatarOption, EventReview, Event, Task, UserProfile, Skill, Notification
from .forms import EventReviewForm, EventForm, SkillManagementForm, ReadOnlyEventForm, TaskForm, NotificationManagementForm
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.views import View
from django.contrib.auth.models import Group
from django.contrib import messages


class HomeView(LoginRequiredMixin, TemplateView):
    """ Home View
    Redirects unauthenticated users to landing page.
    """
    
    template_name = 'home.html'

    def get_context_data(self,*args, **kwargs):
        context = super(HomeView, self).get_context_data(*args,**kwargs)
        if self.request.user.groups.filter(name='Volunteer').exists():
            context['events'] = Event.objects.filter(admin=self.request.user)
        elif self.request.user.groups.filter(name='Admin').exists():
            context['events'] = Event.objects.filter(admin=self.request.user)

        context['events_fields'] = ["name","description","location","date","admin","urgency_display"]
        context['events_headers'] = ["Name","Description","Location","Date","Organizer","Urgency"]
        return context

    login_url = '/'
    def handle_no_permission(self):
        return redirect(self.get_login_url())


class LandingView(TemplateView):
    """ Landing View
    Redirects authenticated users to home page.
    """
    template_name = 'landing.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    

# Event views:
class EventCreateView(AccessMixin, CreateView):
    """Event Create View
    Form for creating a new Event.

    Only accessible for Admin group members.
    """
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    extra_context = {'view_type': 'create'}

    def dispatch(self, request, *args, **kwargs):
        """Handles authorization
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Admin").exists():
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('home')
    

class EventDetailView(LoginRequiredMixin, DetailView):
    """Event Detail View
    Page showing Event information and child Tasks.

    Requires login to view.
    """
    model = Event
    template_name = 'event_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(event=self.get_object())
        context['tasks_fields'] = ["name","description","attendee_count","capacity","location"]
        context['tasks_headers'] = ["Name","Description","Attendees","Capacity","Location"]
        return context
    

class EventUpdateView(AccessMixin, UpdateView):
    """Event Update View
    Form for updating an existing Event.

    Only accessible for Admin group members.
    """
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    extra_context = {'view_type': 'update'}

    def dispatch(self, request, *args, **kwargs):
        """Handles authorization
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Admin").exists():
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if 'pk' in self.kwargs:
            kwargs = {'pk': self.kwargs['pk']}
            return reverse('view_event', kwargs=kwargs)
        else:
            return reverse('home')


class EventDeleteView(AccessMixin, DeleteView):
    """Event Delete View
    Form for deleting an Event.

    Only accessible for Admin group members.
    """
    model = Event
    template_name = 'event_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        """Handles authorization
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Admin").exists():
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home')


# Task views:
class TaskCreateView(AccessMixin, CreateView):
    """Task Create View
    Form for creating a new Task.

    Only accessible for Admin group members.
    """
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    extra_context = {'view_type': 'create'}

    def dispatch(self, request, *args, **kwargs):
        """Handles authorization
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Admin").exists():
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'event_id' in self.kwargs:
            context['event'] = Event.objects.get(id=self.kwargs['event_id'])
            
        return context
    
    
    def form_valid(self, form):
        if 'event_id' in self.kwargs:
            form.instance.event = Event.objects.get(id=self.kwargs['event_id'])
        return super().form_valid(form)


    def get_success_url(self):
        if 'event_id' in self.kwargs:
            kwargs = {'pk': self.kwargs['event_id']}
            return reverse('view_event', kwargs=kwargs)
        else:
            return reverse('home')


class TaskDetailView(LoginRequiredMixin, DetailView):
    """Task Detail View
    Page showing Task information and child Tasks.

    Requires login to view.
    """
    model = Task
    template_name = 'task_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attendees'] = self.get_object().attendees.all()
        context['attendees_fields'] = ["get_full_name", "profile.get_skill_names"]
        context['attendees_headers'] = ["Full Name", 'Skills']
        return context


class TaskUpdateView(AccessMixin, UpdateView):
    """Task Update View
    Form for updating an existing Task.

    Only accessible for Admin group members.
    """
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    extra_context = {'view_type': 'update'}

    def dispatch(self, request, *args, **kwargs):
        """Handles authorization
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Admin").exists():
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if 'pk' in self.kwargs:
            kwargs = {'pk': self.kwargs['pk']}
            return reverse('view_task', kwargs=kwargs)
        else:
            return reverse('home')
 

class TaskDeleteView(AccessMixin, DeleteView):
    """Task Delete View
    Form for deleting an Task.

    Only accessible for Admin group members.
    """
    model = Task
    template_name = 'task_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        """Handles authorization
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Admin").exists():
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home')


class EventReviewCreateView(LoginRequiredMixin, CreateView):
    """ Event Review Create View
    Redirects unauthenticated users to login page.
    """
    login_url = "/login/"
    model = EventReview
    form_class = EventReviewForm
    template_name = 'event_review_form.html'
    extra_context = {'view_type': 'create'}

    def get_success_url(self):
        return redirect('home')

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class EventReviewUpdateView(LoginRequiredMixin, UpdateView):
    """ Event Review Update View
    Redirects unauthenticated users to login page.
    """
    login_url = "/login/"
    model = EventReview
    form_class = EventReviewForm
    template_name = 'event_review_form.html'
    extra_context={'view_type': 'update'}

    def get_success_url(self):
        return redirect('home')

    


class TaskHistoryView(LoginRequiredMixin, TemplateView):
    
    template_name = 'task_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
     
        context['tasks'] = self.request.user.tasks.all()
        context['tasks_fields'] = ["name","description","attendee_count","capacity","location"]
        context['tasks_headers'] = ["Name","Description","Attendees","Capacity","Location"]
        return context
    

class NotificationCreateView(LoginRequiredMixin, CreateView):
        model = Notification
        form_class = NotificationManagementForm
        template_name = 'notification_management.html'
        extra_context = {'view_type': 'create'}

        def get_success_url(self):
            return redirect('home').url #idk where to redirect yet will change later


class SkillManagementCreateView(LoginRequiredMixin, CreateView):
        model = Skill
        form_class = SkillManagementForm
        template_name = 'skill_management.html'
        extra_context = {'view_type': 'create'}

        def get_success_url(self):
            return redirect('skill_browser').url #idk where to redirect yet will change later


class SkillManagementUpdateView(LoginRequiredMixin, UpdateView):
    model = Skill
    form_class = SkillManagementForm
    template_name = 'skill_management.html'
    extra_context = {'view_type': 'update'}

    def get_success_url(self):
        return redirect('skill_browser').url #idk where to redirect yet will change later


class event_browser(LoginRequiredMixin, TemplateView):
    
    template_name = 'event_browser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        context['events_fields'] = ["name","description","location","date","admin","urgency_display"]
        context['events_headers'] = ["Name","Description","Location","Date","Organizer","Urgency"]
        return context

class NotificationInboxView(LoginRequiredMixin, TemplateView):
    template_name = 'inbox.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # Only notifications for events the user is attending
        notifications = Notification.objects.filter(event__attendees=user).distinct()

        context['notifications'] = notifications
        return context

# def inbox(request: HttpRequest) -> HttpResponse:
#     """ Notifications inbox page.

#     :param HttpRequest reqest: The request from the client's browser.
#     :return HttpReponse: The response to the client.
#     """
#     context: dict = {'test_key': 'test_value'}
#     return render(request, 'inbox.html', context)


def skill_browser(request: HttpRequest) -> HttpResponse:
    """ Skill browser page.

    :param HttpRequest request: The request from the client's browser.
    :return HttpResponse: The response to the client.
    """
    skills = Skill.objects.all()  # fetch all Skill objects
    context: dict = {'skills': skills}  # pass them to the template
    return render(request, 'skill_browser.html', context)


def volunteer_history(request: HttpRequest) -> HttpResponse:
    """ Default page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'volunteer_history.html', context)

def matching_form(request: HttpRequest) -> HttpResponse:
    """ Default page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'matching_form.html', context)

class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)

        context.update({
            "profile": profile,
            "name": profile.name,
            "address1": profile.address1,
            "address2": profile.address2,
            "city": profile.city,
            "state": profile.state,
            "zipcode": profile.zipcode,
            "email": profile.email,  
            "phone": profile.phone,  
            "preferences": profile.preferences,
            "start_availability": profile.start_availability,
            "end_availability": profile.end_availability,
            "skills": ", ".join(skill.name for skill in profile.skills.all()),
        })
        return context

class AccountManagementView(LoginRequiredMixin, View):

    def get(self, request):
        skills = Skill.objects.all()  
        profile, created = UserProfile.objects.get_or_create(user=request.user) 
        avatars = AvatarOption.objects.all()
        return render(request, "profile_management.html", {"profile": profile, "skills": skills, "avatars": avatars})

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        profile.name = request.POST.get("name", profile.name)
        profile.address1 = request.POST.get("address1", profile.address1)
        profile.address2 = request.POST.get("address2", profile.address2)
        profile.city = request.POST.get("city", profile.city)
        profile.state = request.POST.get("state", profile.state)
        profile.zipcode = request.POST.get("zipcode", profile.zipcode)
        profile.email = request.POST.get("email", profile.email)  
        profile.phone = request.POST.get("phone", profile.phone)  
        profile.preferences = request.POST.get("preferences", profile.preferences)
        start_availability = request.POST.get("start_availability", "").strip()
        end_availability = request.POST.get("end_availability", "").strip()

        profile.start_availability = start_availability if start_availability else profile.start_availability
        profile.end_availability = end_availability if end_availability else profile.end_availability

        skill_ids = request.POST.getlist("skills")
        skills = Skill.objects.filter(id__in=skill_ids)
        profile.skills.set(skills)

        avatar_id = request.POST.get("avatar")
        if avatar_id:
            try:
                avatar = AvatarOption.objects.get(id=avatar_id)
                profile.avatar = avatar
            except AvatarOption.DoesNotExist:
                pass

        profile.save()

        return redirect("account")