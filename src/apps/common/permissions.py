from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedAndHasRole(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsAdmin(IsAuthenticatedAndHasRole):
    message = "You must be an admin user to perform this action."

    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
               hasattr(request.user, 'role') and request.user.role.lower() == 'admin'

class IsEntrepreneur(IsAuthenticatedAndHasRole):
    message = "You must be an entrepreneur to perform this action."

    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
               hasattr(request.user, 'role') and request.user.role.lower() == 'entrepreneur' and \
               request.method in ['GET', 'POST', 'PUT']

class IsUser(IsAuthenticatedAndHasRole):
    message = "You must have a 'user' role to perform this action."

    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
               hasattr(request.user, 'role') and request.user.role.lower() == 'user' and \
               request.method in SAFE_METHODS

class IsUserOnly(IsAuthenticatedAndHasRole):
    message = "Only users with role 'user' can become entrepreneurs."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'user'
