from django.contrib import admin
from .models import CourseModel,VideoModel,WeekModule,ReviewModel
# Register your models here.

@admin.register(CourseModel)

class CourseRegister(admin.ModelAdmin):
    list_display=["title","instructor","department","amount","created_at"]
    ordering=["created_at"]

@admin.register(WeekModule)

class WeekRegister(admin.ModelAdmin):
    list_display=["course","name"]

@admin.register(VideoModel)

class VideoRegister(admin.ModelAdmin):
    list_display=["course","week","title","video_file","description","uploaded_at"]

@admin.register(ReviewModel)
class ReviewAdmin(admin.ModelAdmin):
    list_display=["course","user","rating","body","created_on"]
