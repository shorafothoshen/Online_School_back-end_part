from django.db import models

# Create your models here.
class DepartmentModel(models.Model):
    name=models.CharField(max_length=75, blank=True, null= True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name