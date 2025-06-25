from rest_framework.permissions import BasePermission, SAFE_METHODS


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.role == 'admin':
            return True

        if user.role == 'entrepreneur':
            return request.method in ['GET', 'POST', 'PUT']

        if user.role == 'user':
            return request.method in SAFE_METHODS

        return False
