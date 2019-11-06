from django.contrib import admin
from .models import Post, Warren, Follower

# Register your models here.


admin.site.register(Post)
admin.site.register(Warren)
admin.site.register(Follower)