from django.shortcuts import render
from catalog.models import Product, Contacts


def home(request):
    products = Product.objects.order_by('created_at')[:5]
    return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    contacts_display = Contacts.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts.html', {'contact_display': contacts_display})
