from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from accounts.forms import MyUserCreationForm
from accounts.models import Profile


class RegisterView(CreateView):
    model = User
    template_name = "registration.html"
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


class UserProfileView(DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_object'

    def get_context_data(self, **kwargs):
        return super(UserProfileView, self).get_context_data(**kwargs)


class UserIndexView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    context_object_name = 'user_object'
    template_name = 'user_index.html'
    paginate_by = 8
    paginate_orphans = 0
    permission_required = "auth.view_user"

    # def has_permission(self):
    #     return super().has_permission() and self.request.user in self.get_object().project.users.all()

