from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post, ViewCount
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

        return render(request, 'post/index.html', {'posts': posts})


class PostView(View):

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        try:
            ViewCount.objects.get(ip_address=ip, post=post)
        except ViewCount.DoesNotExist:
            ViewCount(post=post, ip_address=ip).save()

        return render(request, 'post/post.html', {'post': post})

class AboutView(View):
    def get(self, request):
        return render(request, 'post/about.html')

class ContactsView(View):
    def get(self, request):
        return render(request, 'post/contacts.html')
