from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')  # Перенаправляем на свою страницу входа
        return view_func(request, *args, **kwargs)
    return _wrapped_view
