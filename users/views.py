import random
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserForm, UserProfileForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()
        to = self.object.email
        subject = 'Поздравляем с регистрацией!'
        message = 'Вы зарегистрировались на нашем сайте E-shop!'
        from_email = settings.EMAIL_HOST_USER
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[to]
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_passwor = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    to = request.user.email
    subject = 'Вы сменили пароль!'
    message = f'Ваш новый пароль: {new_passwor}'
    from_email = settings.EMAIL_HOST_USER
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[to]
    )
    request.user.set_password(new_passwor)
    request.user.save()
    return redirect(reverse('catalog:home'))

