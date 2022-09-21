from django.shortcuts import render, get_object_or_404

from posts.forms import EmailPostForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.http import Http404


class PostListView(ListView):
    """Alternative post list view"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "posts/list.html"


def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.status.PUBLISHED)
    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
        else:
            form = EmailPostForm()
        return render(request, "posts/share.html", {"post": post, "form": form})


def post_list(request):
    post_list = Post.published.all()
    # pagination with 3 posts per page
    paginator = Paginator(post_list, 3)  # 3 posts in each page
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # if page_number is not on integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "posts/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    try:
        post = get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day,
        )
    except Post.DoesNotExist:
        raise Http404("No Post found")
    return render(request, "posts/detail.html", {"post": post})
