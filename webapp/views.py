from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, RedirectView

from webapp.forms import TaskForm
from webapp.models import Task


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.order_by("status")
        return render(request, 'index.html', {'tasks': tasks})


class CreateView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'create_task.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            new_task = form.save()
            return redirect('task_view', pk=new_task.pk)
        return render((request, 'add_view', {"form": form}))


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


class EditView(TemplateView):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        form = TaskForm(initial={'title': task.title,
                                 'description': task.description,
                                 'status': task.status,
                                 'type': task.type})
        return render(request, 'task_edit.html', {'task': task, 'form': form})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.title = form.cleaned_data.get('title')
            task.description = form.cleaned_data.get('description')
            task.status = form.cleaned_data.get('status')
            task.type = form.cleaned_data.get('type')
            task.save()
            return redirect("task_view", pk=task.pk)
        return render(request, 'task_edit.html', {'task': task, 'form': form})
