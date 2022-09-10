from operator import imod
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create(
            username="testuser",
            email="test@email.com",
            password="secrect",
        )
        cls.post = Post.objects.create(
            author = cls.user,
            title = "Test Blog Post",
            body="Nice body content",
            
        )
        
    
    def test_post_model(self):
        self.assertEqual(self.post.author.username,"testuser")
        self.assertEqual(self.post.title,"Test Blog Post")
        self.assertEqual(self.post.body,"Nice body content")
        self.assertEqual(str(self.post),"Test Blog Post")
        