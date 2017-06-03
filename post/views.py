from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post

def index(request):
    return HttpResponse('Index function view')

class IndexView(View):
    def get(self, request):
        posts = Post.objects.filter(is_published=True)
        return render(request, 'post/index.html', {'posts': posts})


class PostView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'post/post.html', {'post': post})
