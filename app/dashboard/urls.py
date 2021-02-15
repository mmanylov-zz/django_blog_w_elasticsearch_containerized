from django.conf.urls import url

from .views import IndexView, PostView, PostEdit, PostDelete

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^index/$', IndexView.as_view()),
    url(r'^post/(?P<slug>[-\w]+).html/$', PostView.as_view(), name='post-view'),
    url(r'^post-edit/(?P<slug>[-\w]+).html/$', PostEdit.as_view(), name='post-edit'),
    url(r'^post-delete/(?P<slug>[-\w]+).html/$', PostDelete.as_view(), name='post-delete'),
]
