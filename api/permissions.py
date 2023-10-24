from rest_framework.permissions import BasePermission
from rest_framework import permissions

# This custom permission had to be written since this particular one is not provided by drf
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        
        return bool(request.user and request.user.is_staff)
    


class IsOrderOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or (request.user.is_authenticated and request.user.is_staff)

