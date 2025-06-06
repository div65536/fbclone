from rest_framework import permissions


class ReadOnlyPermissionOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated


class EditForObjectAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False


class UserEditPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user == obj or request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
