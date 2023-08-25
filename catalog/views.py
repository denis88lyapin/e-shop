from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from catalog.form import ProductForm
from catalog.models import Product, Contacts, Version
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

    def get_queryset(self):
        return super().get_queryset().order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for product in context['object_list']:
            active_version = Version.objects.filter(product=product, version_activ=True).first()
            if active_version:
                product.active_version_number = active_version.version_num
                product.active_version_name = active_version.version_name
            else:
                product.active_version_number = None
                product.active_version_name = None

        return context


class ProductDetailViev(DetailView):
    model = Product
    template_name = 'catalog/product.html'
    extra_context = {
        'title': 'Товар'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_version = Version.objects.filter(product=self.object, version_activ=True).first()
        if active_version:
            context['active_version_number'] = active_version.version_num
            context['active_version_name'] = active_version.version_name
        else:
            context['active_version_number'] = None
            context['active_version_name'] = None

        return context


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
