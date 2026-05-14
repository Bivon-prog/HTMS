"""Round-robin assignment within mission + routing department (SRS 3.4)."""
from django.db.models import Count, Q

from apps.authentication.models import User


def assign_round_robin(ticket) -> bool:
    """
    If the ticket has no agent, assign the active agent in the mission + routing_department
    with the fewest active workload. Returns True if an assignment was made.
    """
    if ticket.assigned_agent_id:
        return False

    dept = ticket.category.routing_department
    agents = (
        User.objects.filter(
            role='Agent',
            mission=ticket.mission,
            department=dept,
            is_active=True,
        )
        .annotate(
            load=Count(
                'assigned_tickets',
                filter=Q(
                    assigned_tickets__status__in=['Open', 'Assigned', 'In_Progress'],
                ),
            )
        )
        .order_by('load', 'id')
    )
    agent = agents.first()
    if not agent:
        return False

    ticket.assigned_agent = agent
    if ticket.status == 'Open':
        ticket.status = 'Assigned'
    ticket.save(update_fields=['assigned_agent', 'status', 'updated_at'])
    return True
