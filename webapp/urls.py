from django.urls import path

from webapp.views import IndexView, CreateView, TaskView, DeleteView, EditView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('add/', CreateView.as_view(template_name='create_task.html'), name='add_view'),
    path('task/<int:pk>/', TaskView.as_view(template_name="task_view.html"), name="task_view"),
    path('del/<int:pk>/', DeleteView.as_view(template_name="delete_view.html"), name="delete_view"),
    path('edit/<int:pk>/', EditView.as_view(template_name="task_edit.html"), name="task_edit"),
]
