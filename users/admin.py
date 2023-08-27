from django.contrib import admin
from users.models import User


admin.site.register(User)
# @admin.register(User)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'email', 'first_name', 'phone', 'country',)
