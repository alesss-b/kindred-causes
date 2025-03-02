from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from .models import EventReview
from .forms import EventReviewForm

def login(request: HttpRequest) -> HttpResponse:
    """ Login page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    
    return render(request, 'login.html')


def landing(request: HttpRequest) -> HttpResponse:
    """ Landing page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'landing.html', context)


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


def home(request: HttpRequest) -> HttpResponse:
    """ Home page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'home.html', context)


def inbox(request: HttpRequest) -> HttpResponse:
    """ Notifications inbox page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'inbox.html', context)


def account(request: HttpRequest) -> HttpResponse:
    """ Account page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context = {
        # Public
        "name": request.session.get("name", "John Doe"),
        "city": request.session.get("city", "New York"),
        "state": request.session.get("state", "NY"),
        "start_availability": request.session.get("start_availability", "January 1, 1989"),
        "end_availability": request.session.get("end_availability", "January 1, 1999"),
        "skills": ", ".join(request.session.get("skills", ["Eating", "Sleeping", "Programming"])),

        # Private
        "email": request.session.get("email", "john.doe@example.com"),
        "address": request.session.get("address1", "123 Main St"),
        "address2": request.session.get("address2", "None"),
        "zip_code": request.session.get("zipcode", "11223"),
        "phone": request.session.get("phone", "(123) 456-7890"),
    }
    return render(request, "account.html", context)

def account_management(request: HttpRequest) -> HttpResponse:
    """ Account page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    if request.method == "POST":
        # Public
        request.session["name"] = request.POST.get("name", "John Doe")
        request.session["city"] = request.POST.get("city", "New York")
        request.session["state"] = request.POST.get("state", "NY")
        request.session["start_availability"] = request.POST.get("start_availability", "January 1, 1989")
        request.session["end_availability"] = request.POST.get("end_availability", "January 1, 1999")
        request.session["skills"] = request.POST.getlist("skills")

        # Private
        request.session["email"] = request.POST.get("email", "john.doe@example.com")
        request.session["address"] = request.POST.get("address1", "123 Main St")
        request.session["address2"] = request.POST.get("address2", "None")
        request.session["zip_code"] = request.POST.get("zipcode", "11223")
        request.session["phone"] = request.POST.get("phone", "(123) 456-7890")

        request.session.modified = True

        return redirect("account") # Redirect to the account page
    
    return render(request, "profile_management.html")

def index(request: HttpRequest) -> HttpResponse:
    """ Default page.

    :param HttpRequest reqest: The request from the client's browser.
    :return HttpReponse: The response to the client.
    """
    context: dict = {'test_key': 'test_value'}
    return render(request, 'root.html', context)



class EventReviewCreateView(CreateView):
    model = EventReview
    form_class = EventReviewForm
    template_name = 'event_review_form.html'
    extra_context = {'view_type': 'create'}

    def get_success_url(self):
        return redirect('home').url
        # return redirect('event_detail', pk=self.object.pk).url

# class EventReviewDetailView(DetailView):
#     model = EventReview
#     template_name = 'event_review_detail.html'
#     context_object_name = 'event_review'


class EventReviewUpdateView(UpdateView):
    model = EventReview
    form_class = EventReviewForm
    template_name = 'event_review_form.html'
    extra_context={'view_type': 'update'}

    def get_success_url(self):
        return redirect('home').url
        # return redirect('event_detail', pk=self.object.pk).url
