from rest_framework.permissions import BasePermission
from .models import Professional, User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return bool(request.user.is_authenticated and request.user.is_admin)


class ProfessionalsPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated: 
            if request.user.is_admin ==  True or request.user.is_prof == True:
                return True