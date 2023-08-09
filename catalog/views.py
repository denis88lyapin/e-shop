from django.shortcuts import render
from django.urls import reverse_lazy
from catalog.models import Product, Contacts
from django.views.generic import ListView, DetailView, TemplateView, CreateView


class HomeView(TemplateView):
    template_name = 'catalog/home.html'
    model = Product
    extra_context = {
        'title': 'E-shop - Главная',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.order_by('-created_at')[:5]
        return context_data


def contacts(request):
    context = {
        'contact_display': Contacts.objects.first(),
        'title': 'Обратная связь',
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts.html', context)


class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/products.html'
    paginate_by = 1
    extra_context = {
        'title': 'Наши товары',
    }


class ProductDetailViev(DetailView):
    model = Product
    template_name = 'catalog/product.html'
    extra_context = {
        'title': 'Товар'
    }


class CreateProductView(CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/create_product.html'
    success_url = reverse_lazy('catalog:home')
    extra_context = {
        'title': 'Добавить товар',
    }
