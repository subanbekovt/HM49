from django.urls import path

from webapp.views import IndexView, TaskView, DeleteView, EditView, ProjectIndexView, ProjectView, \
    ProjectCreate, TaskCreate

urlpatterns = [
    path('tasks', IndexView.as_view(), name="index"),
    path('project/<int:pk>/task/add/', TaskCreate.as_view(), name='add_view'),
    path('task/<int:pk>/', TaskView.as_view(template_name="task/task_view.html"), name="task_view"),
    path('task/del/<int:pk>/', DeleteView.as_view(template_name="task/delete_task.html"), name="delete_view"),
    path('task/edit/<int:pk>/', EditView.as_view(template_name="task/task_edit.html"), name="task_edit"),
    path('', ProjectIndexView.as_view(), name="project_index"),
    path('project/add/', ProjectCreate.as_view(), name='project_add'),
    path('project/<int:pk>/', ProjectView.as_view(template_name="project/view.html"), name="project_view"),
]
