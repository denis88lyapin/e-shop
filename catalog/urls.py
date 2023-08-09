from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contacts, HomeView, ProductsListView, ProductDetailViev, CreateProductView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('products/', ProductsListView.as_view(), name='products'),
    path('product/<int:pk>', ProductDetailViev.as_view(), name='product'),
    path('create_product/', CreateProductView.as_view(), name='create_product')
]
