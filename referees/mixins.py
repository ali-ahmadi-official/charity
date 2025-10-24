from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from functools import wraps

class SuperAdminRequiredMixin:
    """میکسین برای بررسی سوپرادمین بودن در ویوهای کلاس‌بیست"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

def superadmin_required(view_func):
    """دکوراتور بررسی سوپرادمین بودن در FBV"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view
