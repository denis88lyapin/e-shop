from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from catalog.form import ProductForm, VersionForm, ProductCuttedForm, CategoryForm
from catalog.models import Product, Contacts, Version, Category
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.services import get_categories_cache, get_product_list


class HomeView(ListView):
    template_name = 'catalog/home.html'
    model = Product
    extra_context = {
        'title': 'E-shop - Главная',
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = super().get_queryset().order_by('-created_at', 'pk')[:5]
        else:
            queryset = super().get_queryset().filter(
                status=Product.STATUS_PUBLISH
            )
        return queryset



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
    paginate_by = 10
    extra_context = {
        'title': 'Наши товары',
    }

    def get_queryset(self):
        queryset = get_product_list(request=self.request)
        return queryset

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff:
    #         queryset = super().get_queryset()
    #     else:
    #         queryset = super().get_queryset().filter(
    #             status=Product.STATUS_PUBLISH
    #         )
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for product in context['object_list']:
            active_version = Version.objects.filter(product=product, version_activ=True).last()
            if active_version:
                product.active_version_number = active_version.version_num
                product.active_version_name = active_version.version_name
            else:
                product.active_version_number = None
                product.active_version_name = None

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'
    extra_context = {
        'title': 'Товар'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_version = Version.objects.filter(product=self.object, version_activ=True).last()
        if active_version:
            context['active_version_number'] = active_version.version_num
            context['active_version_name'] = active_version.version_name
        else:
            context['active_version_number'] = None
            context['active_version_name'] = None

        return context


class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    extra_context = {
        'title': 'Добавить товар',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version_form'] = VersionForm()
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        version_form = VersionForm(self.request.POST)
        if version_form.is_valid():
            version = version_form.save(commit=False)
            version.product = self.object
            version.save()

        return redirect(self.get_success_url())


class UpdateProductView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/update_product.html'
    permission_required = 'catalog.change_product'
    success_url = reverse_lazy('catalog:home')
    extra_context = {
        'title': 'Изменить товар',
    }

    def test_func(self):
        user = self.request.user
        product = self.get_object()

        if product.owner == user or user.is_staff:
            return True
        return False

    def get_form_class(self):
        product = self.get_object()
        user = self.request.user

        if user.is_staff:
            return ProductCuttedForm
        elif product.owner == user:
            return ProductForm

        return super().get_form_class()

    def handle_no_permission(self):
        return redirect(reverse_lazy('catalog:home'))


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            return redirect(reverse('catalog:home'))
        return self.object

    def get_success_url(self):
        return reverse('catalog:detail_product', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user

        if user == self.object.owner:
            VersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
            if self.request.method == 'POST':
                context_data['formset'] = VersionFormSet(self.request.POST, instance=self.object)
            else:
                context_data['formset'] = VersionFormSet(instance=self.object)
        return context_data

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.owner:
            formset = self.get_context_data()['formset']
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)

    # def form_invalid(self, form, version_form):
    #     return self.render_to_response(self.get_context_data(form=form, version_form=version_form))


class DeleteProductView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:home')

 # CategoryCreateView, CategoryUpdateView, CategoryDeleteView


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    extra_context = {
        'title': 'Категории',
    }

    def get_queryset(self):
        queryset = get_categories_cache()
        return queryset
    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(*args, **kwargs)
    #     context_data['object_list'] =


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')
    extra_context = {
        'title': 'Добавить категорию',
    }


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')
    extra_context = {
        'title': 'Изменить категорию',
    }


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy("catalog:category_list")










# class UpdateProductView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'catalog/update_product.html'
#     permission_required = 'catalog.change_product'
#     success_url = reverse_lazy('catalog:home')
#     extra_context = {
#         'title': 'Изменить товар',
#     }
#
#     def test_func(self):
#         product = self.get_object()
#         user = self.request.user
#
#         if user.is_staff or product.owner == user:
#             return True
#
#         return False
#
#     def get_success_url(self):
#         return reverse('catalog:detail_product', args=[self.object.pk])
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['version_form'] = VersionForm()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         version_form = VersionForm(request.POST)
#
#         if form.is_valid() and version_form.is_valid():
#             return self.form_valid(form, version_form)
#         else:
#             return self.form_invalid(form, version_form)
#
#     def form_valid(self, form, version_form):
#         self.object = form.save()
#
#         if self.request.user.is_staff:
#             # Модератор может отменять публикацию
#             if self.request.POST.get('cancel_publish'):
#                 self.object.status = Product.STATUS_MODERATED
#
#             # Модератор и владелец могут менять описание и категорию
#             if self.request.user.has_perm('catalog.change_product_description'):
#                 self.object.description = form.cleaned_data['description']
#             if self.request.user.has_perm('catalog.change_product_category'):
#                 self.object.category = form.cleaned_data['category']
#
#             # Владелец может менять все поля, кроме статуса
#             if self.object.owner == self.request.user:
#                 self.object.name = form.cleaned_data['name']
#                 self.object.image = form.cleaned_data['image']
#                 self.object.price = form.cleaned_data['price']
#
#             self.object.save()
#             return redirect(self.get_success_url())
#
#     def form_invalid(self, form, version_form):
#         return self.render_to_response(self.get_context_data(form=form, version_form=version_form))
