from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        return bool(request.user.is_authenticated and request.user.is_admin)
