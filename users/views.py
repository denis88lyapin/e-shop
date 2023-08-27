import random
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView
from config import settings
from users.forms import UserForm, UserProfileForm
from users.models import User
from django.contrib import messages


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
        user = form.save(commit=False)
        user.is_active = False
        vrf_token = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        confirm_url = self.request.build_absolute_uri(reverse('users:confirm', args=[vrf_token]))
        user.vrf_token = vrf_token
        user.save()
        to = user.email
        subject = 'Регистрация в нашем проекте E-shop!'
        message = f'Для регистрации перейдите по ссылке {confirm_url}!'
        from_email = settings.EMAIL_HOST_USER
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[to]
        )
        return super().form_valid(form)


class ConfirmRegistrationView(View):
    def get(self, request, vrf_token):
        try:
            user = User.objects.get(vrf_token=vrf_token)
            user.is_active = True
            user.vrf_token = None
            user.save()
        except User.DoesNotExist:
            messages.error(request, "Ошибка: Пользователь с указанным "
                                    "токеном не найден. Пройдите регистрацию снова.")
        return redirect('users:register')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    to = request.user.email
    subject = 'Вы сменили пароль!'
    message = f'Ваш новый пароль: {new_password}'
    from_email = settings.EMAIL_HOST_USER
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[to]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:home'))


def reset_password(request):
    """Сгенерировать новый пароль для пользователя если пароль забыли"""
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user = User.objects.get(email=user_email)
            new_password = "".join([str(random.randint(0, 9)) for _ in range(12)])
            user.set_password(new_password)
            user.save()

            subject = "Смена пароля на платформе E-shop"
            message = f"Ваш новый пароль: {new_password}"
            from_email = settings.EMAIL_HOST_USER
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[user_email]
            )
            return redirect(reverse("users:login"))
        except User.DoesNotExist:
            return render(request, 'users/change_password.html', {'error_message': 'User not found'})
    return render(request, 'users/change_password.html')
