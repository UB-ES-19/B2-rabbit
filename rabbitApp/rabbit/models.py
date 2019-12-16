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

    @property
    def get_score(self):
        return self.scores.filter(value=True).count() - self.scores.filter(value=False).count()


class Comment(models.Model):
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')

    @property
    def get_score(self):
        return self.scores.filter(value=True).count() - self.scores.filter(value=False).count()


class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')


class Subscribe(models.Model):
    subscriber = models.ForeignKey(User, related_name='subscribing', on_delete=models.CASCADE)
    subscribing = models.ForeignKey(Warren, related_name='subscriber', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscribing', 'subscriber')


class Score(models.Model):
    value = models.BooleanField()
    post = models.ForeignKey(Post, related_name='scores', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='scores', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, related_name='scores', on_delete=models.CASCADE)

    class Meta:
        unique_together = (['user', 'post', 'comment'])


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='log')
    time = models.DateTimeField(auto_now_add=True)
    os = models.TextField()
    browser = models.TextField()

    def __str__(self):
        return 'User %s connected at %s from %s running on %s' % (self.user.username, self.time.__str__(), self.browser
                                                                  , self.os)

