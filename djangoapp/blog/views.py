from typing import Any

from blog.models import Page, Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

POST_PER_PAGE = 2

class PostListView(ListView):
    #model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    #ordering = '-pk',
    paginate_by = POST_PER_PAGE
    queryset = Post.objects.get_published() # type: ignore

    # def get_queryset(self):
    #     query_set = super().get_queryset()
    #     query_set = query_set.filter(is_published=True)
    #     return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context

# Create your views here.
# def index(request):
#     posts = Post.objects.get_published() 

#     paginator = Paginator(posts, POST_PER_PAGE )
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj' : page_obj,
#             'page_title': 'Home -',
#         }
#     )

# def created_by(request, author_pk):    
#     user = User.objects.filter(pk=author_pk).first()    

#     if user is None:
#         raise Http404()
    
#     user_full_name = user.username 

#     if(user.first_name):
#         user_full_name= f'{user.first_name} {user.last_name}'
    
#     page_title = user_full_name + ' posts - '

#     posts = (
#         Post.objects.get_published()
#         .filter(created_by__pk=author_pk)
#         ) 

#     paginator = Paginator(posts, POST_PER_PAGE )
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj' : page_obj,
#             'page_title': page_title,
#         }
#     )

class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context =  {}

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        
        author_pk = self.kwargs.get('author_pk')       
        user = User.objects.filter(pk=author_pk).first()    

        if user is None:
            raise Http404()
        
        self._temp_context.update(
            {
                'author_pk':author_pk,
                'user':user,
            }
        )
        
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['author_pk'])
        return qs
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

          
        user = self._temp_context['user']       
    
        user_full_name = user.username 

        if(user.first_name):
            user_full_name= f'{user.first_name} {user.last_name}'

        page_title = user_full_name + ' posts - '

        context.update({
            'page_title': page_title,
        })

        return context


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_title = f'{self.object_list[0].category.name} - ' # type: ignore

        context.update({
            'page_title': page_title,
        })

        return context

# def category(request, slug):
#     posts = (
#         Post.objects.get_published()
#         .filter(category__slug=slug)
#         )     

#     paginator = Paginator(posts, POST_PER_PAGE )
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404
    
#     page_title = f'{page_obj[0].category.name} - '
    

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj' : page_obj,
#             'page_title': page_title,
#         }
#     )

class TagListView(PostListView):
     
     allow_empty = False

     def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        
        page_title = f'{self.object_list[0].tags.filter(slug=slug).first().name} - ' # type: ignore

        context.update({
            'page_title': page_title,
        })

        return context

# def tag(request, slug):
#     posts = (
#         Post.objects.get_published()
#         .filter(tags__slug=slug)
#         ) 

#     paginator = Paginator(posts, POST_PER_PAGE )
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404
    
#     page_title = f'{page_obj[0].tags.filter(slug=slug).first().name} - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj' : page_obj,
#             'page_title': page_title,
#         }
#     )

class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search','').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(title__icontains=self._search_value) |
            Q(excerpt__icontains=self._search_value) |
            Q(content__icontains=self._search_value)             
        )[0:POST_PER_PAGE]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        
        page_title = f'{self._search_value[:20]} - '
        
        context.update({
            'search_value': self._search_value,
            'page_title': page_title,
        })

        return context
    
    def get(self, request, *args: Any, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)

# def search(request):
#     search_value =request.GET.get('search', '').strip()
#     posts = (
#         Post.objects.get_published()
#         .filter(
#             Q(title__icontains=search_value) |
#             Q(excerpt__icontains=search_value) |
#             Q(content__icontains=search_value) 
#         )[0:POST_PER_PAGE]
#     ) 

#     page_title = f'{search_value[:20]} - '
   
#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj' : posts,
#             'search_value': search_value,
#             'page_title': page_title,
#         }
#     )

class PageDetailView(DetailView):
    model = Page
    template_name  = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name='page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        page = self.get_object()

        page_title = f'{page.title} - '       # type: ignore       
        
        context.update({            
            'page_title': page_title,
        })

        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
        )

# def page(request, slug):
#     current_page = (
#         Page.objects
#         .filter(is_published=True)
#         .filter(slug=slug)
#         .first()
#         ) 
#     if current_page is None:
#         raise Http404
    
#     page_title = f'{current_page.title} - '

#     return render(
#         request,
#         'blog/pages/page.html',
#         {
#             'page':current_page,
#             'page_title': page_title,
#         }
#     )

def post(request, slug):
    current_post = (
        Post.objects.get_published()
        .filter(slug=slug)
        .first()
        ) 
    
    if current_post is None:
        raise Http404
    
    page_title = f'{current_post.title} - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': current_post,
            'page_title': page_title,
        }
    )