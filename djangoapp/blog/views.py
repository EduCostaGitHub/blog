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

def page(request):
    return render(
        request,
        'blog/pages/page.html'
    )

def post(request):
    return render(
        request,
        'blog/pages/post.html'
    )