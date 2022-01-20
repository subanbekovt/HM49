from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from webapp.base import FormView as CustomFormView
from webapp.forms import TaskForm
from webapp.models import Task


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.order_by("status")
        return render(request, 'index.html', {'tasks': tasks})


class CreateView(CustomFormView):
    form_class = TaskForm
    template_name = "create_task.html"

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect("task_view", pk=self.object.pk)
    # def get(self, request, *args, **kwargs):
    #     form = TaskForm()
    #     return render(request, 'create_task.html', {'form': form})
    #
    # def post(self, request, *args, **kwargs):
    #     form = TaskForm(data=request.POST)
    #     if form.is_valid():
    #         new_task = form.save()
    #         return redirect('task_view', pk=new_task.pk)
    #     return render(request, 'create_task.html', {'form': form})


class TaskView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        context['task'] = task
        return context


class DeleteView(TemplateView):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        return render(request, 'delete_view.html', {'task': task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        task.delete()
        return redirect('index')


# class EditView(TemplateView):
#     def get(self, request, *args, **kwargs):
#         task = get_object_or_404(Task, pk=kwargs.get('pk'))
#         form = TaskForm(initial={'title': task.title,
#                                  'description': task.description,
#                                  'status': task.status,
#                                  'type': task.types})
#         return render(request, 'task_edit.html', {'task': task, 'form': form})
#
#     def post(self, request, *args, **kwargs):
#         task = get_object_or_404(Task, pk=kwargs.get('pk'))
#         form = TaskForm(data=request.POST)
#         if form.is_valid():
#             types = form.cleaned_data.get('types')
#             task.types.set(types)
#             task.title = form.cleaned_data.get('title')
#             task.description = form.cleaned_data.get('description')
#             task.status = form.cleaned_data.get('status')
#             task.type = form.cleaned_data.get('type')
#             task.save()
#             return redirect("task_view", pk=task.pk)
#         return render(request, 'task_edit.html', {'task': task, 'form': form})

class EditView(FormView):
    form_class = TaskForm
    template_name = "task_edit.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super(EditView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={"pk": self.task.pk})

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get("pk"))
