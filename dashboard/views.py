from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from post.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    return HttpResponse('Index function view')

class IndexView(View):
    def get(self, request):
        posts = Post.published.all()
        paginator = Paginator(posts, 3)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        return render(request, 'dashboard/post/index.html', {'posts': posts})


class PostView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'dashboard/post/view.html', {'post': post})

class PostEdit(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'dashboard/post/edit.html', {'post': post})

class PostDelete(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'dashboard/post/delete.html', {'post': post})

class PostCreate(View):
    def get(self, request):
        post = Post()
        return render(request, 'dashboard/post/create.html', {'post': post})
