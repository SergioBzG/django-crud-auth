from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    # In this class we can customize the admin page, eg: in this case we want to show the created field. Without this class, the created field from Task model is not shown
    readonly_fields = ('created',) # This is a read only field, so the user can not modify it

# Register your models here.
admin.site.register(Task, TaskAdmin)
