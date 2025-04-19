from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .forms import UserRegistrationForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('account_management')

    def form_valid(self, form):
        user = form.save()

        volunteer_group = Group.objects.get(name="Volunteer")
        user.groups.add(volunteer_group)

        login(self.request, user) 
        return super().form_valid(form)