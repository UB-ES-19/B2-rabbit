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
    profile_img = models.ImageField(upload_to=get_image_filename_warren, null=True)
    landscape_img = models.ImageField(upload_to=get_image_filename_warren, null=True)

    def __str__(self):
        return 'w/' + self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    warren = models.ForeignKey(Warren, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(null=True)
    img = models.ImageField(upload_to=get_image_filename_post, null=True)


class Comment(models.Model):
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')


class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')


class Suscribe(models.Model):
    suscriber = models.ForeignKey(User, related_name='suscribing', on_delete=models.CASCADE)
    suscribing = models.ForeignKey(Warren, related_name='suscriber', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('suscribing', 'suscriber')

class Report(models.Model):
    cause = models.IntegerField()
    post = models.ForeignKey(Post, related_name='reported', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reporting', on_delete=models.CASCADE)

    class Meta:
        unique_together = (['user', 'post'])