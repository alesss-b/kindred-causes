from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, TemplateView
from .models import EventReview, Event, UserProfile, Skill
from .forms import EventReviewForm, EventManagementForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import re


class HomeView(LoginRequiredMixin, TemplateView):
    """ Home View
    Redirects unauthenticated users to landing page.
    """
    template_name = 'home.html'

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
        return redirect('home').url
        # return redirect('event_detail', pk=self.object.pk).url


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
        return redirect('home').url
        # return redirect('event_detail', pk=self.object.pk).url


class EventManagementCreateView(CreateView):
        model = Event
        form_class = EventManagementForm
        template_name = 'event_management.html'
        extra_context = {'view_type': 'create'}

        def get_success_url(self):
            return redirect('event_browser').url


class EventManagementUpdateView(UpdateView):
    model = Event
    form_class = EventManagementForm
    template_name = 'event_management.html'
    extra_context = {'view_type': 'update'}

    def get_success_url(self):
        return redirect('event_browser').url


def event_browser(request: HttpRequest) -> HttpResponse:
    """ Event browser page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'event_browser.html', context)


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
        return render(request, "profile_management.html", {"profile": profile, "skills": skills})

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

        profile.save()

        return redirect("account") 