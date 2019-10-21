from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
import os


# Create your models here.
from rabbitApp import settings


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


def get_image_filename(instance, filename):
    post_id = instance.id
    return "images/%s" % post_id + "/" + filename


class DescriptionPost(Post):
    description = models.TextField(max_length=255, blank=True)


class ImgPost(Post):
    img = models.ImageField(upload_to=get_image_filename)


class LinkPost(Post):
    link = models.URLField()
