from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Нужны права администратора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsModerator(permissions.BasePermission):
    message = 'Нужны права модератора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsSuperuser(permissions.BasePermission):
    message = 'Нужны права администратора Django'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
