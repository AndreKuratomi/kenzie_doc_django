from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return bool(request.user.is_authenticated and request.user.is_admin)


class ProfessionalsPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin ==  True:
            return True

        return request.user.is_authenticated and str(request.user.council_number) == str(request.data['council_number'])
