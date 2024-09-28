from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.EnrolledCourseModel)

class EnrollAdmin(admin.ModelAdmin):
    list_display=["user","course","transaction_id","payment_status","enroll_date"]