from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def agent_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'agent_profile'):
            return view_func(request, *args, **kwargs)
        return redirect('no_permission')  # Redirige vers une page d'erreur ou login
    return _wrapped_view
