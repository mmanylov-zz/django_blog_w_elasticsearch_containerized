from django.conf.urls import url

from .views import IndexView, PostView, AboutView, ContactsView

app_name = 'post'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^index/$', IndexView.as_view()),
    url(r'^about/$', AboutView.as_view()),
    url(r'^contacts/$', ContactsView.as_view()),
    url(r'^post/(?P<post_id>\d+)/$', PostView.as_view(), name='post'),
]
