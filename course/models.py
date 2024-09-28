from django.db import models
from teacher.models import TeacherModel
from accounts.models import User
from department.models import DepartmentModel

RATING = (
    (1, "⭐"),
    (2, "⭐⭐"),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐"),
)

class CourseModel(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(TeacherModel, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)
    amount = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="course/images", blank=True, null=True)

    def __str__(self):
        return self.title

class WeekModule(models.Model):
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, related_name="weeks", blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

class VideoModel(models.Model):
    course=models.ForeignKey(CourseModel,on_delete=models.CASCADE, related_name="coursevideos", blank=True, null=True)
    week = models.ForeignKey(WeekModule, on_delete=models.CASCADE, related_name="videos", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to="course/videos")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ReviewModel(models.Model):
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews",blank=True,null=True)
    rating = models.IntegerField(choices=RATING)
    body = models.TextField(default="", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_on']
