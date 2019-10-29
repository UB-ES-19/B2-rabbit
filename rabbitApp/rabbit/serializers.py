from rest_framework import serializers
from .models import Post, Warren


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','user','creation_date','warren','description','link','img']


class WarrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warren
        fields = ['name','description','creation_date','creator','profile_img','landscape_img']