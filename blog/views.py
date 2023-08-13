from django.urls import reverse_lazy, reverse
from blog.models import Blog
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from django.core.mail import send_mail
from decouple import config


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'body', 'image', 'is_published')
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body', 'image', 'is_published')

    def get_success_url(self):
        return reverse('blog:detail', args=[self.object.slug])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:index')


class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Наш блог'
    }

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['object_list'] = Blog.objects.order_by('-created_at').filter(is_published=True)
        return context_data


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object:
            self.object.views_count += 1
            self.object.save()

            if self.object.views_count == 100:
                subject = 'Поздравление с достижением 100 просмотров'
                message = f'Статья "{self.object.title}" достигла 100 просмотров.'
                from_email = config('EMAIL_HOST_USER')
                recipient_list = ['denis88lyapin@gmail.com']
                send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

        return self.object
