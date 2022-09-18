from django.shortcuts import render
from .models import Post
from .serializers import PostSerializers

from rest_framework import generics,permissions


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    
    
    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser)
    queryset = Post.objects.all()
    serializer_class = PostSerializers