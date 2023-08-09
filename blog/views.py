from django.shortcuts import render
from blog.models import Blog
from django.views.generic import ListView

class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Наш блог'
    }

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['object_list'] = Blog.objects.order_by('-created_at')
        return context_data
