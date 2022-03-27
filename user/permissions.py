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

        # if request.method != "POST" or request.method == "DELETE" or request.method == "PUT":
        # return request.user.is_authenticated and str(request.user.council_number) == str(request.data['council_number'])
        # return request.user.is_authenticated and request.user.is_prof ==  True and str(request.user.council_number)
        
        # professional = Professional.objects.filter(email=request.user)
        # print("====permissions======")
        # print(request.user)
        # # print(request.user.email)

        # return bool(request.user.is_authenticated and request.user.is_prof ==  True)
        # if request.user.is_authenticated and request.user.is_admin ==  False:
        #     if request.user.is_authenticated and request.user.is_prof ==  True:
        #         return True
            # if professional
            # return request.user.is_authenticated and len(str(request.user.council_number)) > 0
                # return True

        # professional = Professional.objects.get(council_number=council_number)
        # print(professional.council_number)

        # us = Professional.objects.get(user=request.user)
        # print(us.council_number)