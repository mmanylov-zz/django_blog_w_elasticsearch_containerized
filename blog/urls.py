from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^9104da4ec86c28b6ee2bc84fb2870a659c170864/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard', app_name='dashboard')),
    url(r'', include('post.urls', namespace='post', app_name='post')),
]
