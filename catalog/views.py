from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from catalog.forms import ProductForm
from catalog.models import Product, Contacts


def home(request):
    context = {
        'products': Product.objects.order_by('created_at')[:5],
        'title': 'E-sop - Главная'
    }

    return render(request, 'catalog/home.html', context)


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


def products(request):
    products = Product.objects.order_by('created_at')
    paginator = Paginator(products, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': 'Наши товары',
    }

    return render(request, 'catalog/products.html', context)


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'catalog/product.html', context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm()
    context = {
        'form': form,
        'title': 'Добавить товар',
    }
    return render(request, 'catalog/create_product.html', context)
