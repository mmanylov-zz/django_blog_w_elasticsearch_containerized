from django.contrib import admin
from post.models import Post
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_at', 'status')
    list_filter = ('status', 'created_at', 'published_at')
    search_fields = ('title', 'markdown')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ['status', 'published_at']

    # def get_form(self, request, obj=None, **kwargs):
    #     self.exclude = ("body", )
    #     form = super(PostAdmin, self).get_form(request, obj, **kwargs)
    #     return form


admin.site.register(Post, PostAdmin)
