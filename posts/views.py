from django.shortcuts import render
from .models import Post
from .serializers import PostSerializers

from rest_framework import generics


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers