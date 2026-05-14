from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users (Mission_Admin or HQ_Super_Admin).
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['Mission_Admin', 'HQ_Super_Admin']
        )


class IsHQSuperAdmin(permissions.BasePermission):
    """
    Allows access only to HQ Super Admin users.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'HQ_Super_Admin'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows access only to the resource owner or admin users.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can access any object
        if request.user.role in ['Mission_Admin', 'HQ_Super_Admin']:
            return True
        
        # Check if the object has a user field and if it matches the current user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if the object is the user itself
        if hasattr(obj, 'id') and obj.id == request.user.id:
            return True
        
        return False


class IsMissionUserOrAdmin(permissions.BasePermission):
    """
    Allows access only to users from the same mission or admin users.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'HQ_Super_Admin':
            return True

        from apps.tickets.models import Ticket
        if isinstance(obj, Ticket):
            from apps.tickets.access import user_can_access_ticket
            return user_can_access_ticket(request.user, obj)

        if hasattr(obj, 'mission'):
            return obj.mission == request.user.mission

        if hasattr(obj, 'requester') and hasattr(obj.requester, 'mission'):
            return obj.requester.mission == request.user.mission

        return False


class CanAssignTickets(permissions.BasePermission):
    """
    Allows access only to users who can assign tickets.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.can_assign_tickets()
        )


class CanViewAllMissionTickets(permissions.BasePermission):
    """
    Allows access only to users who can view all tickets in their mission.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.can_view_all_mission_tickets()
        )
