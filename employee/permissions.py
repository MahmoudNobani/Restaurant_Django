from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission class for Django REST Framework to control access to resources.

    Allows read-only access to any authenticated user, but grants write access only to the original author
    or admin members.

    Attributes:
        - has_permission(self, request, view): Determines if the user is authenticated (general use)
        - has_object_permission(self, request, view, obj): Determines if the user is author or admin and give it the desired actions 
        (specific usage)
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated to give it access

        Args:
            request: The incoming HTTP request.
            view: The DRF view being accessed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission for a specific object.
        for author he can edit (put/patch)
        admin can do anything including deleting

        Args:
            request: The incoming HTTP request.
            view: The DRF view being accessed.
            obj: The object the permission is being checked against (found using pk in the call)

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if bool(request.user and request.user.is_staff):
            return True
        if request.method in ["PUT","PATCH"] or request.method in permissions.SAFE_METHODS:
            return obj.pk == request.user.pk
        return False