from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def solo_admins(vista_func):
    @wraps(vista_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("login")
        return vista_func(request, *args, **kwargs)
    return wrapper