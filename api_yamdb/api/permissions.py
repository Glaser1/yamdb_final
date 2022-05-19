
from rest_framework import permissions


class AuthorOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        if (request.user.is_authenticated
                and request.user.role == 'moderator'):
            return True
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)


class UserReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'username' in view.kwargs:
            if view.kwargs['username'] == 'me':
                return True
        return (
            request.user.role == 'admin'
            or request.user.is_superuser
        )


class AdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff
                or (request.user.is_authenticated
                    and request.user.role == 'admin')
                )
