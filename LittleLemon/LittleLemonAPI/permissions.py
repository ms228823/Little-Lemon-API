"""
---------------------------------------------------------------------
Custom Permissions for the Little Lemon API
---------------------------------------------------------------------

These permissions are designed to restrict access to specific views
based on the user's group membership. The permissions can be applied
to views to ensure that only users in the appropriate group can access
certain resources.

---------------------------------------------------------------------
"""

from rest_framework.permissions import BasePermission

# Custom permission that checks if the user belongs to the 'Manager' group
class IsManager(BasePermission):
    """
    Allows access only to users who are part of the 'Manager' group.
    """
    def has_permission(self, request, view):
        # Check if the user is in the 'Manager' group
        return request.user.groups.filter(name="Manager").exists()


# Custom permission that checks if the user belongs to the 'Delivery Crew' group
class IsDeliveryCrew(BasePermission):
    """
    Allows access only to users who are part of the 'Delivery Crew' group.
    """
    def has_permission(self, request, view):
        # Check if the user is in the 'Delivery Crew' group
        return request.user.groups.filter(name="Delivery Crew").exists()
