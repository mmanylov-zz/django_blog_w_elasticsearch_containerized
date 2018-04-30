from django.urls import path, re_path
from .views import IndexView, PostView, SearchView#, AboutView, ContactsView

app_name = 'post'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search', SearchView.as_view(), name='search'),
    #url(r'^index/$', IndexView.as_view()),
    #url(r'^about/$', AboutView.as_view()),
    #url(r'^contacts/$', ContactsView.as_view()),
    re_path(r'^post/(?P<slug>[-\w]+).html$', PostView.as_view(), name='post'),
]
