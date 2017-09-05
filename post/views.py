from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    return HttpResponse('Index function view')

class IndexView(View):
    def get(self, request):
        posts = Post.objects.published()
        paginator = Paginator(posts, 2)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        return render(request, 'post/index.html', {'posts': posts})


class PostView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'post/post.html', {'post': post})

class AboutView(View):
    def get(self, request):
        return render(request, 'post/about.html')

class ContactsView(View):
    def get(self, request):
        return render(request, 'post/contacts.html')
