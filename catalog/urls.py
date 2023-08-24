from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contacts, HomeView, ProductsListView, ProductDetailViev, CreateProductView, UpdateProductView, DeleteProductView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('products/', ProductsListView.as_view(), name='products'),
    path('product/<int:pk>/detail', ProductDetailViev.as_view(), name='detail_product'),
    path('product/<int:pk>/update', UpdateProductView.as_view(), name='update_product'),
    path('product/<int:pk>/delete', DeleteProductView.as_view(), name='delete_product'),
    path('create_product/', CreateProductView.as_view(), name='create_product')
]
