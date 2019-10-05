from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=255)
    description = models.TextField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)