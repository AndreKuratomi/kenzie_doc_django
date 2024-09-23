from rest_framework.permissions import BasePermission
import ipdb


class AppointmentPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)


class PatientSelfOrAdminPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        if not request.user.is_prof and obj.user == request.user:
            return True
        return False


class ProfessionalSelfOrAdminPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        if request.user.is_prof and obj.user == request.user:
            return True
        return False