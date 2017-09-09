from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard', app_name='dashboard')),
    url(r'', include('post.urls', namespace='post', app_name='post')),
]
