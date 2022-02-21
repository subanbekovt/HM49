from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.forms import TaskForm, SearchForm
from webapp.models import Task, Project


class IndexView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task/index.html'
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
        return queryset.order_by("status")

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


class TaskCreate(PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task/create_task.html"
    permission_required = 'webapp.add_task'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        task = form.save(commit=False)
        task.project_id = project.id
        task.save()
        form.save_m2m()
        return redirect('webapp:project_view', pk=project.pk)

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        return super().has_permission() and self.request.user in project.users.all()


class TaskView(DetailView):
    template_name = 'task/task_view.html'
    model = Task


class TaskDelete(PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = "task/delete_task.html"
    permission_required = "webapp.delete_task"

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.project_id})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()


class EditView(PermissionRequiredMixin, UpdateView):
    model = Task
    template_name = "task/task_edit.html"
    form_class = TaskForm
    permission_required = "webapp.change_task"

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()
