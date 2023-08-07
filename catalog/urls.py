from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contacts, home, products, product, create_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('products/', products, name='products'),
    path('product/<int:pk>', product, name='product'),
    path('create_product/', create_product, name='create_product')
]
