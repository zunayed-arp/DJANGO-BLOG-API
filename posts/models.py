from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class Post(models.Model):
    STATUS_CHOICES = (("draft", "Draft"), ("published", "Published"),)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title
