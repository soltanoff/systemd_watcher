from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow admins to edit it."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff
