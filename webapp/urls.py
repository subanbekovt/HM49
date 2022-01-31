from django.urls import path

from webapp.views import IndexView, CreateView, TaskView, DeleteView, EditView, ProjectIndexView, ProjectView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('add/', CreateView.as_view(template_name='task/create_task.html'), name='add_view'),
    path('task/<int:pk>/', TaskView.as_view(template_name="task/task_view.html"), name="task_view"),
    path('del/<int:pk>/', DeleteView.as_view(template_name="task/delete_task.html"), name="delete_view"),
    path('edit/<int:pk>/', EditView.as_view(template_name="task/task_edit.html"), name="task_edit"),
    path('project/', ProjectIndexView.as_view(), name="project_index"),
    path('project/<int:pk>/', ProjectView.as_view(template_name="project/view.html"), name="project_view"),
]
