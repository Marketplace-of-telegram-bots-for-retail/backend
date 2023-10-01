from rest_framework import permissions


class AuthorCanEditAndDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        del view
        return (
            obj.user == request.user
            or request.method in permissions.SAFE_METHODS
        )


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user
        )
