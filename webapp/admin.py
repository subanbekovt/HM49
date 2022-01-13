from django.contrib import admin
from webapp.models import Task, Status, Type


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'type']
    list_filter = ['status', 'type']
    search_fields = ['title', 'status', 'type']
    fields = ['title', 'description', 'status', 'type', 'created_at', 'updated_at']
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
