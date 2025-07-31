from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class SuperUserRequiredMixin(UserPassesTestMixin):
    """
    این میکسین اجازه دسترسی فقط به سوپریوزرها می‌دهد.
    """
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied("شما دسترسی لازم را ندارید.")
