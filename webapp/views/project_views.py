from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import SearchForm, ProjectForm
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


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project/create.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('webapp:project_index')

    def form_valid(self, form):
        value = form.save(commit=False)
        value.save()
        value.users.set((self.request.user.id, ))
        form.save_m2m()
        return super().form_valid(form)


class ProjectEdit(LoginRequiredMixin, UpdateView):
    form_class = ProjectForm
    template_name = "project/edit.html"
    model = Project


class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "project/delete_project.html"

    def get_success_url(self):
        return reverse('webapp:project_index')

