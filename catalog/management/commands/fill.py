import json
from django.core.management import BaseCommand
from catalog.models import Category, Product, Contacts


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        category_dict = {}

        for item in data:
            if item['model'] == 'catalog.category':
                category = Category.objects.create(**item['fields'])
                category_dict[item['pk']] = category
            elif item['model'] == 'catalog.contacts':
                Contacts.objects.create(**item['fields'])

        for item in data:
            if item['model'] == 'catalog.product':
                category_id = item['fields'].pop('category')
                category = category_dict.get(category_id)
                Product.objects.create(category=category, **item['fields'])
