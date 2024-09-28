from django.contrib import admin
from . models import TeacherModel
# Register your models here.

@admin.register(TeacherModel)

class TeacherAdmin(admin.ModelAdmin):
    list_display=["get_first_name", "department","bio","Country","City"]

    def get_first_name(self, obj):
        return obj.user.first_name