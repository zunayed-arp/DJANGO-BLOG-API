from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.http import Http404


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "posts/list.html"


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "posts/list.html", {"page": page, "posts": posts})


def post_detail(request, id):
    try:
        post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    except Post.DoesNotExist:
        raise Http404("No Post found")
    return render(request, "posts/detail.html", {"post": post})
