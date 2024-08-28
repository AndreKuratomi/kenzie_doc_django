from rest_framework.permissions import BasePermission
from .models import Professional, User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return bool(request.user.is_authenticated and request.user.is_admin)


class IsJustLogged(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
        

class PatientSelfOrAdminPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and not request.user.is_prof and obj.user == request.user:
            return True
        return False


class ProfessionalSelfOrAdminPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_prof and obj.user == request.user:
            return True
        return False
