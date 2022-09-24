from django.shortcuts import render, get_object_or_404

from posts.forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.http import Http404
from django.views.decorators.http import require_POST
from taggit.models import Tag


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    comment_data = request.POST
    form = CommentForm(data=comment_data)
    if form.is_valid():
        # create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the port to the comment
        comment.post = post
        # save the comment to the database
        comment.save()
    return render(
        request, "posts/comment.html", {"post": post, "comment": comment, "form": form}
    )


class PostListView(ListView):
    """Alternative post list view"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "posts/list.html"


from django.core.mail import send_mail


def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        # Form was submitted
        aa = {}
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            print("aa", aa)
            print("cd", cd)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" f"{post.title}"
            message = (
                f"Read{post.title} as {post_url}\n\n"
                f"{cd['name']}\\'s comments: {cd['comments']}"
            )
            send_mail(subject, message, "zunayeduapcse@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
        # print(form)

    return render(
        request, "posts/share.html", {"post": post, "form": form, "sent": sent}
    )


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
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
    return render(request, "posts/list.html", {"posts": posts, "tag": tag})


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
        # List of active comments for this post
        comments = post.comments.filter(active=True)
        # Form for users to comments
        form = CommentForm()
    except Post.DoesNotExist:
        raise Http404("No Post found")
    return render(
        request, "posts/detail.html", {"post": post, "comments": comments, "form": form}
    )
