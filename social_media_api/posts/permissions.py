from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: allow read-only for any request, but only allow owners to edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any request.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only to the object's owner.
        # obj is Post or Comment and both have an "author" attribute.
        return getattr(obj, 'author', None) == request.user
