from django.contrib import admin
from .models import Post, Warren, Follower, Suscribe, Report
from .models import Post, Warren, Follower, Subscribe, Score

# Register your models here.


admin.site.register(Post)
admin.site.register(Warren)
admin.site.register(Follower)
admin.site.register(Suscribe)
admin.site.register(Report)
admin.site.register(Score)
