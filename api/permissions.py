from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.models import Role


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == Role.ADMIN:
            return True
        return False


class GeneralPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == Role.ADMIN


class IsStuff(BasePermission):
    def has_permission(self, request, view):
        if request.user.role in (Role.ADMIN, Role.MODERATOR):
            return True
        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user == obj.author:
            return True

        if request.user.role in (Role.ADMIN, Role.MODERATOR):
            return True

        return False
