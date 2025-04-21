from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, TemplateView
from .models import AvatarOption, EventReview, Event, Task, UserProfile, Skill
from .forms import EventReviewForm, EventManagementForm, SkillManagementForm, ReadOnlyEventManagementForm
from django.contrib.auth.mixins import LoginRequiredMixin
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
        context['events_fields'] = ["name","description","location","date","admin","urgency"]
        context['events_headers'] = ["Name","Description","Location","Date","Organizer", "Urgency"]
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

# EventReview Model Forms:
# class EventReviewDetailView(DetailView):
#     model = EventReview
#     template_name = 'event_review_detail.html'
#     context_object_name = 'event_review'

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
        # return redirect('event_detail', pk=self.object.pk).url

    def form_invalid(self, form):
        print("FORM INVALID")
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
        # return redirect('event_detail', pk=self.object.pk).url


class EventManagementCreateView(CreateView):
    model = Event
    form_class = EventManagementForm
    template_name = 'event_management.html'
    extra_context = {'view_type': 'create'}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('home')


class EventManagementUpdateView(UpdateView):
    model = Event
    form_class = EventManagementForm
    template_name = 'event_management.html'
    extra_context = {'view_type': 'update'}

    def get_success_url(self):
        return redirect('home')


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(event=self.get_object())
        context['tasks_fields'] = ["name","description","attendee_count","capacity","location"]
        context['tasks_headers'] = ["Name","Description","Attendees","Capacity","Location"]
        return context
    

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = self.get_object().skills
        context['skills_fields'] = ["name","description"]
        context['skills_headers'] = ["Name","Description"]
        return context


class SkillManagementCreateView(CreateView):
        model = Skill
        form_class = SkillManagementForm
        template_name = 'skill_management.html'
        extra_context = {'view_type': 'create'}

        def get_success_url(self):
            return redirect('skill_browser').url #idk where to redirect yet will change later


class SkillManagementUpdateView(UpdateView):
    model = Skill
    form_class = SkillManagementForm
    template_name = 'skill_management.html'
    extra_context = {'view_type': 'update'}

    def get_success_url(self):
        return redirect('skill_browser').url #idk where to redirect yet will change later

def event_browser(request: HttpRequest) -> HttpResponse:
    """ Event browser page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    sort = request.GET.get('sort', 'date')
    allowed_sorts = ['name', '-name', 'date', '-date', 'urgency', '-urgency']

    if sort not in allowed_sorts:
        sort = 'date'

    events = Event.objects.all().order_by(sort)
    context = {
        'events': events,
        'current_sort': sort
    }

    return render(request, 'event_browser.html', context)

def skill_browser(request: HttpRequest) -> HttpResponse:
    """ Skill browser page.

    :param HttpRequest request: The request from the client's browser.
    :return HttpResponse: The response to the client.
    """
    skills = Skill.objects.all()  # fetch all Skill objects
    context: dict = {'skills': skills}  # pass them to the template
    return render(request, 'skill_browser.html', context)


def event_preview(request: HttpRequest) -> HttpResponse:
    """ Event preview page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'event_preview.html', context)
    
def event_management(request: HttpRequest) -> HttpResponse:
    """ Event Management page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'event_management.html', context)
    

def user_registration(request: HttpRequest) -> HttpResponse:
    """ User registration page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'user_registration.html', context)


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


def inbox(request: HttpRequest) -> HttpResponse:
    """ Notifications inbox page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'inbox.html', context)


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