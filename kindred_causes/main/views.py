from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView
from .models import AvatarOption, EventReview, Event, Task, UserProfile, Skill, Notification
from .forms import EventReviewForm, EventForm, SkillManagementForm, ReadOnlyEventForm, TaskForm, NotificationManagementForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.views import View
from django.contrib.auth.models import Group
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class HomeView(LoginRequiredMixin, TemplateView):
    """ Home View
    Redirects unauthenticated users to landing page.
    """
    
    template_name = 'home.html'

    def get_context_data(self,*args, **kwargs):
        context = super(HomeView, self).get_context_data(*args,**kwargs)
        if self.request.user.groups.filter(name='Volunteer').exists():
            context['events'] = self.request.user.events.all()
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
        if self.request.user.groups.filter(name='Volunteer').exists():
            context['tasks'] = self.request.user.tasks.filter(event=self.get_object())
        elif self.request.user.groups.filter(name='Admin').exists():
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


def generate_event_report(request, pk):
    event = Event.objects.get(pk=pk)
    tasks = event.tasks.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="event_report_{event.id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 50

    def draw_line(p, y, txt, font="Helvetica", size=12, bold=False, indent=0):
        if bold:
            p.setFont("Helvetica-Bold", size)
        else:
            p.setFont(font, size)
        p.drawString(50 + indent, y, txt)
        return y - 18

    def get_user_skills(user):
        """Gather all skills from tasks the user is assigned to."""
        skill_set = set()
        for task in user.tasks.all():
            for skill in task.skills.all():
                skill_set.add(skill.name)
        return sorted(skill_set)

    # Event Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Event Report: {event.name}")
    y -= 30

    y = draw_line(p, y, f"Description: {event.description}")
    y = draw_line(p, y, f"Location: {event.location}")
    y = draw_line(p, y, f"Urgency: {event.get_urgency_display()}")
    if event.date:
        y = draw_line(p, y, f"Date: {event.date.strftime('%Y-%m-%d %H:%M')}")
    y = draw_line(p, y, f"Total Capacity: {event.capacity}")
    y = draw_line(p, y, f"Total Attendees: {event.attendee_count}")
    y -= 10

    # Task Breakdown
    y = draw_line(p, y, "Tasks", bold=True, size=14)

    for task in tasks:
        if y < 120:
            p.showPage()
            y = height - 50

        y = draw_line(p, y, f"- {task.name}", bold=True, indent=10)
        y = draw_line(p, y, f"  Description: {task.description}", indent=10)
        y = draw_line(p, y, f"  Location: {task.location}", indent=10)
        y = draw_line(p, y, f"  Capacity: {task.capacity}", indent=10)

        # Required skills
        skills = task.skills.all()
        skills_str = ", ".join([s.name for s in skills]) if skills else "None"
        y = draw_line(p, y, f"  Required Skills: {skills_str}", indent=10)

        # Assigned Users
        y = draw_line(p, y, f"  Assigned Attendees:", indent=10)
        assigned_users = task.attendees.all()
        if not assigned_users:
            y = draw_line(p, y, "    (None)", indent=20)
        else:
            for user in assigned_users:
                full_name = user.get_full_name() or user.username
                user_skills = get_user_skills(user)
                skills_str = f" (Skills: {', '.join(user_skills)})" if user_skills else ""
                y = draw_line(p, y, f"    • {full_name}{skills_str}", indent=20)

                # Previous Events attended by the user (excluding this one)
                previous_events = user.events.exclude(pk=event.pk).order_by('-date')
                if previous_events.exists():
                    for prev_event in previous_events:
                        name_date = f"{prev_event.name} ({prev_event.date.strftime('%Y-%m-%d') if prev_event.date else 'No date'})"
                        y = draw_line(p, y, f"       - {name_date}", indent=30)
                        if y < 100:
                            p.showPage()
                            y = height - 50
                else:
                    y = draw_line(p, y, "       - (No previous events)", indent=30)

                if y < 100:
                    p.showPage()
                    y = height - 50

    p.showPage()
    p.save()
    return response


class JoinEventView(LoginRequiredMixin, TemplateView):
    """Join Event View
    Page confirming that user wants to join the event.

    Requires login.
    """
    template_name = 'confirm_join_event.html'

    def post(self, request, *args, **kwargs):
        if 'event_id' in kwargs:
            event = Event.objects.get(id=self.kwargs['event_id'])
            event.attendees.add(request.user)
            event.save()
        
        return HttpResponseRedirect(reverse('view_event', kwargs={'pk':event.id}))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'event_id' in self.kwargs:
            context['event'] = Event.objects.get(pk=self.kwargs['event_id'])
        context['user'] = self.request.user
        return context
    

class LeaveEventView(LoginRequiredMixin, TemplateView):
    """Leave Event View
    Page confirming that user wants to leave the event.

    Requires login.
    """
    template_name = 'confirm_leave_event.html'

    def post(self, request, *args, **kwargs):
        if 'event_id' in kwargs:
            event = Event.objects.get(id=self.kwargs['event_id'])
            event.attendees.remove(request.user)
            event.save()
            
            for task in request.user.tasks.all():
                task.attendees.remove(request.user)
                task.save()
        
        return HttpResponseRedirect(reverse('view_event', kwargs={'pk':event.id}))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'event_id' in self.kwargs:
            context['event'] = Event.objects.get(pk=self.kwargs['event_id'])
        context['user'] = self.request.user
        return context


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


class TaskDetailView(AccessMixin, DetailView):
    """Task Detail View
    Page showing Task information and child Tasks.

    Only accessible for Admin group members.
    """
    model = Task
    template_name = 'task_details.html'

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
        context['attendees'] = self.get_object().attendees.all()
        context['unassigned_users'] = self.get_object().event.attendees.exclude(pk__in=context['attendees'])
        context['attendees_fields'] = ["get_full_name", "profile.get_skill_names"]
        context['attendees_headers'] = ["Full Name", 'Skills']
        return context
    

class AssignTaskView(AccessMixin, TemplateView):
    """Assign Task View
    Page confirming that user should be assigned to task.

    Only accessible for Admin group members.
    """
    template_name = 'confirm_assign_task.html'

    def dispatch(self, request, *args, **kwargs):
        """Handles authorization
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Admin").exists():
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        if 'user_id' in kwargs and 'task_id' in kwargs:
            user = User.objects.get(pk=self.kwargs['user_id'])
            task = Task.objects.get(id=self.kwargs['task_id'])
            task.attendees.add(user)
            task.save()
        
        return HttpResponseRedirect(reverse('view_task', kwargs={'pk':task.id}))
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'user_id' in self.kwargs:
            context['user'] = User.objects.get(pk=self.kwargs['user_id'])

        if 'task_id' in self.kwargs:
            context['task'] = Task.objects.get(id=self.kwargs['task_id'])
        return context
    


class RemoveTaskView(AccessMixin, TemplateView):
    """Remove Task View
    Page confirming that user should be unassigned from task.

    Only accessible for Admin group members.
    """
    template_name = 'confirm_remove_task.html'

    def dispatch(self, request, *args, **kwargs):
        """Handles authorization
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name="Admin").exists():
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        if 'user_id' in kwargs and 'task_id' in kwargs:
            user = User.objects.get(pk=self.kwargs['user_id'])
            task = Task.objects.get(id=self.kwargs['task_id'])
            task.attendees.remove(user)
            task.save()
        
        return HttpResponseRedirect(reverse('view_task', kwargs={'pk':task.id}))
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'user_id' in self.kwargs:
            context['user'] = User.objects.get(pk=self.kwargs['user_id'])

        if 'task_id' in self.kwargs:
            context['task'] = Task.objects.get(id=self.kwargs['task_id'])
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
    
class NotificationCreateView(CreateView):
    model = Notification
    form_class = NotificationManagementForm
    template_name = 'notification_management.html'
    extra_context = {'view_type': 'create'}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Get event, subject, body from form
            event = form.cleaned_data['event']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            # Loop through event attendees and create notifications
            for attendee in event.attendees.all():
                Notification.objects.create(
                    event=event,
                    recipient=attendee,
                    subject=subject,
                    body=body,
                    is_read=False
                )
            return redirect(self.get_success_url())
        return self.form_invalid(form)

    def get_success_url(self):
        return redirect('inbox').url


class SkillManagementCreateView(CreateView):
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

class NotificationInboxView(TemplateView):
    template_name = 'inbox.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context['inbox'] = Notification.objects.select_related('event') \
            .filter(recipient=user) \
            .order_by('-created_at')

        context['inbox_fields'] = ["is_read", "event", "subject"]
        context['inbox_headers'] = ["Read", "Event", "Subject"]
        return context



class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = 'notification_details.html'
    context_object_name = 'notification'

    def get_queryset(self):
        # Only allow access to notifications the user is part of
        return Notification.objects.filter(
            event__attendees=self.request.user
        ).select_related('event')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=["is_read"])
        return obj

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