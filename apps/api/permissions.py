from rest_framework import permissions

class ReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class EditForObjectAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False