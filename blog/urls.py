from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='index'),
    path('detail/<slug:slug>', BlogDetailView.as_view(), name='detail'),
    path('create/', BlogCreateView.as_view(), name='create'),
    path('update/<slug:slug>', BlogUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>', BlogDeleteView.as_view(), name='delete'),
]
