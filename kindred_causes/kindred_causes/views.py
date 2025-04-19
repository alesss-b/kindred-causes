from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .forms import UserRegistrationForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')  # or whatever your landing page is

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Automatically log in the user
        return super().form_valid(form)