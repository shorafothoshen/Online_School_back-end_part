from django.contrib import admin
from .models import DepartmentModel
# Register your models here.

@admin.register(DepartmentModel)

class DepartmentAdmin(admin.ModelAdmin):
    list_display=["name","slug"]
    prepopulated_fields = {'slug': ('name',)}