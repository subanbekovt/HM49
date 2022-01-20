from django.contrib import admin
from webapp.models import Task, Status, Type


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status']
    list_filter = ['status', 'types']
    search_fields = ['title', 'status', 'types']
    fields = ['title', 'description', 'status', 'types', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['status']
    fields = ['status']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['type']
    fields = ['type']


admin.site.register(Task, TaskAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
