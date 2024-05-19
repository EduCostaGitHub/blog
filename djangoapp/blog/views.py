from blog.models import Post
from django.core.paginator import Paginator
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
        }
    )

def created_by(request, author_pk):
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
        }
    )

def page(request, slug):
    return render(
        request,
        'blog/pages/page.html'
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