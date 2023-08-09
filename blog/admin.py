from django.contrib import admin

from blog.models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'body', 'image', 'is_published', 'views_count',)
    list_filter = ('is_published', 'created_at',)
    search_fields = ('title', 'body',)

