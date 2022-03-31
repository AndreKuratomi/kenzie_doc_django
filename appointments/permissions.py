from rest_framework.permissions import BasePermission


class AppointmentPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)


class AppointmentByIdForProfessionalPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin or request.user.is_prof)
