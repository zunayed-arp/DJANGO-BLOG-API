from django.urls import path
from .views import post_list, post_detail, PostListView

app_name = "posts"

urlpatterns = [
    # path("", post_list, name="post_list"),
    path("", PostListView.as_view(), name="post_list"),
    path("<int:id>/", post_detail, name="post_detail"),
]
