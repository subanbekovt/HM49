from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, RedirectView

from webapp.models import Task


class IndexView(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.order_by("status")
        return render(request, 'index.html', {'tasks': tasks})
