from datetime import timedelta

from django.db.models import Count, F
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.authentication.models import User
from apps.missions.models import Mission
from apps.tickets.access import ticket_list_for_user
from apps.permissions import IsHQSuperAdmin
from apps.tickets.models import Ticket


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_overview(request):
    queryset = ticket_list_for_user(request.user)

    total_tickets = queryset.count()
    open_tickets = queryset.filter(status='Open').count()
    in_progress_tickets = queryset.filter(status='In_Progress').count()
    resolved_tickets = queryset.filter(status='Resolved').count()
    closed_tickets = queryset.filter(status='Closed').count()

    overdue_tickets = queryset.filter(
        sla_due_date__isnull=False,
        sla_due_date__lt=timezone.now(),
        status__in=['Open', 'Assigned', 'In_Progress'],
    ).count()

    priority_stats = {}
    for priority in ['Low', 'Medium', 'High', 'Critical']:
        priority_stats[priority.lower()] = queryset.filter(priority=priority).count()

    status_stats = {
        'open': open_tickets,
        'assigned': queryset.filter(status='Assigned').count(),
        'in_progress': in_progress_tickets,
        'resolved': resolved_tickets,
        'closed': closed_tickets,
    }

    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_tickets = queryset.filter(created_at__gte=seven_days_ago)
    recent_resolved = queryset.filter(resolved_date__gte=seven_days_ago).count()

    thirty_days_ago = timezone.now() - timedelta(days=30)
    resolved_tickets_30_days = queryset.filter(
        resolved_date__gte=thirty_days_ago,
        created_at__gte=thirty_days_ago,
    )

    avg_resolution_time = None
    if resolved_tickets_30_days.exists():
        total_resolution_time = sum(
            (ticket.resolved_date - ticket.created_at).total_seconds() / 3600
            for ticket in resolved_tickets_30_days
            if ticket.resolved_date
        )
        avg_resolution_time = total_resolution_time / resolved_tickets_30_days.count()

    sla_compliant = queryset.filter(
        status__in=['Resolved', 'Closed'],
        resolved_date__isnull=False,
        sla_due_date__isnull=False,
        resolved_date__lte=F('sla_due_date'),
    ).count()

    total_resolved_closed = queryset.filter(status__in=['Resolved', 'Closed']).count()

    sla_compliance_rate = 0
    if total_resolved_closed > 0:
        sla_compliance_rate = (sla_compliant / total_resolved_closed) * 100

    data = {
        'overview': {
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'in_progress_tickets': in_progress_tickets,
            'resolved_tickets': resolved_tickets,
            'closed_tickets': closed_tickets,
            'overdue_tickets': overdue_tickets,
        },
        'by_priority': priority_stats,
        'by_status': status_stats,
        'recent_activity': {
            'new_tickets': recent_tickets.count(),
            'resolved_tickets': recent_resolved,
        },
        'performance': {
            'average_resolution_hours': round(avg_resolution_time, 2) if avg_resolution_time else None,
            'sla_compliance_rate': round(sla_compliance_rate, 2),
        },
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mission_statistics(request):
    if request.user.role != 'HQ_Super_Admin':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

    missions = Mission.objects.all()
    mission_stats = []

    for mission in missions:
        tickets = Ticket.objects.filter(mission=mission)

        stats = {
            'mission_id': mission.id,
            'mission_name': mission.name,
            'country': mission.country,
            'total_tickets': tickets.count(),
            'open_tickets': tickets.filter(status='Open').count(),
            'resolved_tickets': tickets.filter(status='Resolved').count(),
            'overdue_tickets': tickets.filter(
                sla_due_date__isnull=False,
                sla_due_date__lt=timezone.now(),
                status__in=['Open', 'Assigned', 'In_Progress'],
            ).count(),
        }

        mission_stats.append(stats)

    return Response(mission_stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ticket_trends(request):
    queryset = ticket_list_for_user(request.user)

    thirty_days_ago = timezone.now() - timedelta(days=30)
    queryset = queryset.filter(created_at__gte=thirty_days_ago)

    from django.db.models.functions import TruncDate

    trends = (
        queryset.annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    return Response(list(trends))


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def agent_performance(request):
    if request.user.role not in ['Mission_Admin', 'HQ_Super_Admin']:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

    queryset = User.objects.filter(role='Agent')

    if request.user.role == 'Mission_Admin':
        queryset = queryset.filter(mission=request.user.mission)

    agent_stats = []

    for agent in queryset:
        agent_tickets = Ticket.objects.filter(assigned_agent=agent)

        stats = {
            'agent_id': agent.id,
            'agent_name': agent.get_full_name(),
            'total_assigned': agent_tickets.count(),
            'resolved': agent_tickets.filter(status='Resolved').count(),
            'in_progress': agent_tickets.filter(status='In_Progress').count(),
            'overdue': agent_tickets.filter(
                sla_due_date__isnull=False,
                sla_due_date__lt=timezone.now(),
                status__in=['Assigned', 'In_Progress'],
            ).count(),
        }

        resolved_tickets = agent_tickets.filter(status='Resolved')
        if resolved_tickets.exists():
            total_resolution_time = sum(
                (ticket.resolved_date - ticket.created_at).total_seconds() / 3600
                for ticket in resolved_tickets
                if ticket.resolved_date
            )
            stats['average_resolution_hours'] = round(
                total_resolution_time / resolved_tickets.count(), 2
            )
        else:
            stats['average_resolution_hours'] = None

        agent_stats.append(stats)

    return Response(agent_stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsHQSuperAdmin])
def export_dashboard_tickets_csv(request):
    """CSV export of tickets (mission filter optional) — SRS 3.9."""
    import csv
    from io import StringIO
    from django.http import HttpResponse

    from apps.tickets.models import Ticket

    mission_id = request.query_params.get('mission_id')
    qs = Ticket.objects.select_related('mission', 'requester', 'category').all()
    if mission_id:
        qs = qs.filter(mission_id=mission_id)

    buf = StringIO()
    w = csv.writer(buf)
    w.writerow([
        'ticket_number', 'title', 'status', 'priority', 'mission', 'category',
        'requester_email', 'created_at', 'resolved_date',
    ])
    for t in qs.iterator():
        w.writerow([
            t.ticket_number, t.title, t.status, t.priority,
            t.mission.name if t.mission_id else '',
            t.category.name if t.category_id else '',
            t.requester.email if t.requester_id else '',
            t.created_at.isoformat() if t.created_at else '',
            t.resolved_date.isoformat() if t.resolved_date else '',
        ])
    resp = HttpResponse(buf.getvalue(), content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="dashboard_tickets.csv"'
    return resp
