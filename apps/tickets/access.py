"""Ticket visibility rules (SRS 3 / pdf2)."""
from django.db.models import Q

from apps.authentication.models import User


def agent_ticket_visibility_q(user: User) -> Q:
    """Tickets an Agent may list or open (mission Tier-1 or HQ Tier-2 queue)."""
    dept = user.department
    assigned = Q(assigned_agent=user)
    if not dept:
        return assigned

    if user.mission_id:
        dept_queue = Q(
            mission=user.mission,
            category__routing_department=dept,
            status__in=['Open', 'Assigned', 'In_Progress'],
        )
        return assigned | dept_queue

    hq_queue = Q(escalated_to_hq=True, category__routing_department=dept)
    return assigned | hq_queue


def user_can_access_ticket(user: User, ticket) -> bool:
    from .models import Ticket

    if not user.is_authenticated:
        return False
    if user.role == 'HQ_Super_Admin':
        return True
    if user.role == 'Requester':
        return ticket.requester_id == user.id or ticket.beneficiary_id == user.id
    if user.role == 'Mission_Admin':
        return ticket.mission_id == user.mission_id
    if user.role == 'Agent':
        return Ticket.objects.filter(pk=ticket.pk).filter(agent_ticket_visibility_q(user)).exists()
    return False


def ticket_list_for_user(user: User):
    """ORM queryset of tickets visible in list/detail/statistics for ``user``."""
    from .models import Ticket

    qs = Ticket.objects.select_related(
        'requester', 'beneficiary', 'assigned_agent', 'category', 'mission',
    ).prefetch_related('comments', 'attachments')

    if user.role == 'HQ_Super_Admin':
        base = qs
    elif user.role == 'Agent' and not user.mission_id:
        base = qs.filter(agent_ticket_visibility_q(user))
    elif user.mission_id:
        base = qs.filter(mission=user.mission)
    else:
        return qs.none()

    if user.role == 'Requester':
        return base.filter(Q(requester=user) | Q(beneficiary=user))
    if user.role == 'Agent' and user.mission_id:
        return base.filter(agent_ticket_visibility_q(user))
    return base
