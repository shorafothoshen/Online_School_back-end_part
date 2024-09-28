from django.db import models
from course.models import CourseModel
from accounts.models import User
# Create your models here.

class EnrolledCourseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrolled_courses")
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE,blank=True,null=True)
    enroll_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True,null=True)  # For storing the transaction ID
    payment_status = models.CharField(max_length=20, default="PENDING")  # Payment status (optional)
