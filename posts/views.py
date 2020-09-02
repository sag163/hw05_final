import logging
from django.shortcuts import get_object_or_404, render, redirect
from posts.models import Post, Comment, Follow
from group.models import Group
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from users.forms import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


def index(request):
    post_list = Post.objects.select_related("author", 'group').order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {"page": page, 'paginator':paginator})


def group_post(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
    return render(request, "group.html", {"group": group, "page": page, 'paginator':paginator})

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
    else:
        form = PostForm()
    return render(request, "new.html", {"form": form})

def profile(request, username):
    person = get_object_or_404(User, username=username)
    count_post = Post.objects.filter(author=person).count()
    post_list = Post.objects.order_by("-pub_date").filter(author=person).select_related('author', 'group')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    author = User.objects.get(username=username)
    if request.user.is_authenticated:
        follow_status = Follow.objects.filter(user=request.user).filter(author=person)
        if not follow_status:
            follow_stat = None
        else:
            follow_stat = True
        return render(request, "profile.html", {"page": page, 'paginator':paginator, 'username':username, 'author':author, "count_post":count_post, 'follow_stat':follow_stat})
    return render(request, "profile.html", {"page": page, 'paginator':paginator, 'username':username, 'author':author, "count_post":count_post})

def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post_user = Post.objects.filter(author__username=username).filter(pk=post_id)
    count_post = Post.objects.filter(author__username=username).count() 
    post = Post.objects.get(id=post_id)
    items = Comment.objects.filter(post=post_id)
    form = CommentForm()
    return render(request, "post.html", {'post_user':post_user, 'author':author, 'post':post, 'items':items, 'form':form, "count_post":count_post})

  

@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect("post", username=request.user.username, post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("post", username=request.user.username, post_id=post_id)
    return render(request, "new.html", {"form": form, "post": post})       


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            comment= form.save(commit=False)
            comment.author = request.user
            comment.post = post 
            comment.save()
            return redirect("post", username, post_id)
    else:
        form = CommentForm()
    return render(request, 'comments.html', {'form':form, 'post':post}) 


@login_required
def follow_index(request):
    follows = Follow.objects.filter(user=request.user).values('author')
    following_list = Post.objects.filter(author_id__in=follows).order_by("-pub_date")
    paginator = Paginator(following_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
        
    return render(request, "follow.html", {'page':page, 'paginator':paginator})

@login_required
def profile_follow(request, username):
    person = get_object_or_404(User, username=username)
    follow_stat = Follow.objects.filter(user=request.user).filter(author=person)
    if request.user.username != username:
        if  not follow_stat:
            Follow.objects.create(user=request.user, author=person)
            return redirect('profile', username)
        else:
            return redirect('profile', username)
    else:
        return redirect('profile', username)
    

@login_required
def profile_unfollow(request, username):
    person = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user).filter(author=person).delete()
    return redirect ('profile', username=person)

        
def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
        return render(request, "misc/500.html", status=500)

@login_required
def add_like(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.likes += 1
    post.save()
    return redirect('index')


@login_required
def add_dislike(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.dislikes += 1
    post.save()
    return redirect('index')

@login_required
def post_delete(request, username, post_id):
    Post.objects.filter(pk=post_id).delete()
    return redirect('profile', username)