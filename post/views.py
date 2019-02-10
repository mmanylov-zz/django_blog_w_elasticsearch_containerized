from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post, ViewCount
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .search import search
# including Mako template engine dependencies
from mako.template import Template
from mako.lookup import TemplateLookup
from blog.settings import TEMPLATES, BASE_DIR
import os

PAGE_SIZE = 8

class IndexView(View): 
    def get(self, request):
        posts = Post.published.all()
        paginator = Paginator(posts, PAGE_SIZE)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        template_dirs = [os.path.join(BASE_DIR, 'post/templates/post'), os.path.join(BASE_DIR, 'templates')]
        page_lookup = TemplateLookup(directories=template_dirs)
        page_tempalte = Template(filename=os.path.join(BASE_DIR, 'post/templates/post/index_mako.html'), lookup=page_lookup)
        context = dict(
            posts=posts,
            query=''
        )

        return HttpResponse(page_tempalte.render(**context))
        #return render(request, 'post/index.html', {'posts': posts})


class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        if query.strip:
            responseObject = search(query)
            hits = responseObject.hits
            message = "Found " + str(len(hits)) + "matches"
        else:
            hits = []
            message = "Please, input something to search for."

        return render(request, 'post/search.html', {
            'posts': hits,
            'message': message,
            'query': query
        })


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
