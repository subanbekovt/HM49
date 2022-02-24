from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.forms import MyUserCreationForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeForm
from accounts.models import Profile

User = get_user_model()


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
    model = User
    template_name = 'profile.html'
    context_object_name = 'user_object'

    def get_context_data(self, **kwargs):
        return super(UserProfileView, self).get_context_data(**kwargs)


class UserIndexView(PermissionRequiredMixin, ListView):
    model = User
    context_object_name = 'user_object'
    template_name = 'user_index.html'
    paginate_by = 8
    paginate_orphans = 0
    permission_required = "auth.view_user"


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    form_profile_class = ProfileUpdateForm
    template_name = 'update_profile.html'
    context_object_name = 'user_object'

    def get_success_url(self):
        return reverse('accounts:user_profile', kwargs={"pk": self.request.user.pk})

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        profile_form.save()
        return super().form_valid(form)

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == "POST":
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileUpdateForm(**form_kwargs)

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)


class UserPasswordChangeView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_object'

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:user_profile', kwargs={'pk': self.request.user.pk})
