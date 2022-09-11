from django.shortcuts import render
from .models import Post
from .serializers import PostSerializers

from rest_framework import generics


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    
    
    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers