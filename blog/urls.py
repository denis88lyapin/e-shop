from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogListView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='index'),
    # path('contacts/', contacts, name='contacts'),
    # path('products/', ProductsListView.as_view(), name='products'),
    # path('product/<int:pk>', ProductDetailViev.as_view(), name='product'),
    # path('create_product/', CreateProductView.as_view(), name='create_product')
]
