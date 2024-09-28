from django.db import models
from accounts.models import User
from department.models import DepartmentModel
# Create your models here.

class TeacherModel(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher")
    department = models.ForeignKey(DepartmentModel,on_delete=models.CASCADE)
    bio=models.TextField(blank=True, null=True)
    Country=models.CharField(max_length=60,blank=True,null=True)
    City=models.CharField(max_length=100 ,blank=True,null=True)

    def __str__(self):
        return self.user.first_name +" "+self.user.last_name
