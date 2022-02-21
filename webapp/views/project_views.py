from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import SearchForm, ProjectForm, UserForm
from webapp.models import Project, Task


class ProjectIndexView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'project/index.html'
    paginate_by = 8
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by("-pk")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SearchForm()
        if self.search_value:
            context['form'] = SearchForm(initial={"search": self.search_value})
            context['search'] = self.search_value
        return context

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class ProjectView(DetailView):
    template_name = 'project/view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = self.object.projects.order_by("title")
        context['projects'] = projects
        return context


class ProjectCreate(PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'project/create.html'
    form_class = ProjectForm
    permission_required = 'webapp.add_project'

    def get_success_url(self):
        return reverse('webapp:project_index')

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        project.users.set((self.request.user.id, ))
        form.save_m2m()
        return super().form_valid(form)


class ProjectEdit(PermissionRequiredMixin, UpdateView):
    form_class = ProjectForm
    template_name = "project/edit.html"
    model = Project
    permission_required = 'webapp.change_project'

    def has_permission(self):
        return super().has_permission() or self.request.user in self.get_object().users.all() and \
               self.request.user.groups.filter(name='manager').exists()


class ProjectAddUser(PermissionRequiredMixin, UpdateView):
    form_class = UserForm
    template_name = "project/add_user.html"
    model = Project
    permission_required = 'webapp.can_add_users_to_project'

    def has_permission(self):
        return super().has_permission() or self.request.user in self.get_object().users.all() and \
               self.request.user.groups.filter(name='lead').exists()


class ProjectDelete(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = "project/delete_project.html"
    permission_required = 'webapp.delete_project'

    def get_success_url(self):
        return reverse('webapp:project_index')

    def has_permission(self):
        return super().has_permission() or self.request.user in self.get_object().users.all() and \
               self.request.user.groups.filter(name='manager').exists()
