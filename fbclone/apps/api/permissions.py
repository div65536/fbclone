from rest_framework import permissions


class ReadOnlyPermissionOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated


class EditForObjectAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        else:
            return False


class UserEditPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        else:
            return False
