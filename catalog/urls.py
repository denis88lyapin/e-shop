from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (contacts, HomeView, ProductsListView, ProductDetailView, CreateProductView,
                           UpdateProductView, DeleteProductView,  CategoryListView, CategoryCreateView,
                           CategoryUpdateView, CategoryDeleteView)

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('products/', ProductsListView.as_view(), name='products'),
    path('product/<int:pk>/detail', cache_page(60)(ProductDetailView.as_view()), name='detail_product'),
    path('product/<int:pk>/update', UpdateProductView.as_view(), name='update_product'),
    path('product/<int:pk>/delete', DeleteProductView.as_view(), name='delete_product'),
    path('create_product/', CreateProductView.as_view(), name='create_product'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('category_create/', CategoryCreateView.as_view(), name='category_create'),
    path('category_update/<int:pk>', CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>', CategoryDeleteView.as_view(), name='category_delete'),
]
