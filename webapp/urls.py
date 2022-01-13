from django.urls import path

from webapp.views import IndexView, CreateView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('add/', CreateView.as_view(template_name='create_task.html'), name='add_view'),
]
