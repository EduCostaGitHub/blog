from blog.models import Page, Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

POST_PER_PAGE = 9

# Create your views here.
def index(request):
    posts = Post.objects.get_published() 

    paginator = Paginator(posts, POST_PER_PAGE )
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj' : page_obj,
            'page_title': 'Home -',
        }
    )

def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()
    user_full_name = user.username

    if user is None:
        raise Http404()

    if(user.first_name):
        user_full_name= f'{user.first_name} {user.last_name}'
    
    page_title = user_full_name + ' posts -'

    posts = (
        Post.objects.get_published()
        .filter(created_by__pk=author_pk)
        ) 

    paginator = Paginator(posts, POST_PER_PAGE )
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj' : page_obj,
            'page_title': page_title,
        }
    )


def category(request, slug):
    posts = (
        Post.objects.get_published()
        .filter(category__slug=slug)
        ) 

    paginator = Paginator(posts, POST_PER_PAGE )
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj' : page_obj,
        }
    )

def tag(request, slug):
    posts = (
        Post.objects.get_published()
        .filter(tags__slug=slug)
        ) 

    paginator = Paginator(posts, POST_PER_PAGE )
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj' : page_obj,
        }
    )

def search(request):
    search_value =request.GET.get('search', '').strip()
    posts = (
        Post.objects.get_published()
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value) 
        )[0:POST_PER_PAGE]
    ) 
   
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj' : posts,
            'search_value': search_value
        }
    )


def page(request, slug):
    page = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
        ) 
    return render(
        request,
        'blog/pages/page.html',
        {
            'page':page,
        }
    )

def post(request, slug):
    post = (
        Post.objects.get_published()
        .filter(slug=slug)
        .first()
        ) 
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )