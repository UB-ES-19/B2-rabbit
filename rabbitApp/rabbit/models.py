from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


def get_image_filename_post(instance, filename):
    return "images/post/%s" % str(datetime.now()) + filename


def get_image_filename_warren(instance, filename):
    return "images/warren/%s" % instance.name + str(datetime.now()) + filename


class Warren(models.Model):
    name = models.TextField(max_length=50, primary_key=True)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    profile_img = models.ImageField(upload_to=get_image_filename_warren)
    landscape_img = models.ImageField(upload_to=get_image_filename_warren)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    warren = models.ForeignKey(Warren, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(null=True)
    img = models.ImageField(upload_to=get_image_filename_post, null=True)
