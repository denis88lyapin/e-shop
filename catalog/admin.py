from django.contrib import admin

from catalog.models import Category, Product, Contacts, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'status')
    list_filter = ('category', 'status')
    search_fields = ('name', 'description',)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address', 'schedule',)

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_num', 'version_name', 'version_activ')
    list_filter = ('product', 'version_num', 'version_name', 'version_activ')
    search_fields = ('product', 'version_num', 'version_name', 'version_activ')