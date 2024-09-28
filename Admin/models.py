from django.db import models

# Create your models here.

class ContactModel(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=300)
    body=models.TextField()
    create_at=models.DateTimeField(auto_now_add=True)