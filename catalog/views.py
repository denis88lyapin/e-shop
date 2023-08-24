from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from catalog.form import ProductForm
from catalog.models import Product, Contacts
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView


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
    paginate_by = 2
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
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    extra_context = {
        'title': 'Добавить товар',
    }


class UpdateProductView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    extra_context = {
        'title': 'Изменить товар',
    }

    def get_success_url(self):
        return reverse('catalog:detail_product', args=[self.object.pk])


class DeleteProductView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')

