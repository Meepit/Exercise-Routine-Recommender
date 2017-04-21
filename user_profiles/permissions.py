from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow object owners and admins to view / edit an object
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the profile or a superuser
        return obj.user == request.user or request.user.is_superuser


