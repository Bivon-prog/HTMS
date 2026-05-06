from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q, Avg, F
from django.utils import timezone
from datetime import timedelta
from apps.tickets.models import Ticket
from apps.authentication.models import User
from apps.missions.models import Mission


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_overview(request):
    """Get dashboard overview statistics"""
    queryset = Ticket.objects.all()
    
    # Mission isolation for non-HQ users
    if request.user.role != 'HQ_Super_Admin':
        queryset = queryset.filter(mission=request.user.mission)
    
    # Role-based filtering
    if request.user.role == 'Requester':
        queryset = queryset.filter(requester=request.user)
    elif request.user.role == 'Agent':
        queryset = queryset.filter(
            Q(assigned_agent=request.user) | Q(status='Open')
        )
    
    # Basic statistics
    total_tickets = queryset.count()
    open_tickets = queryset.filter(status='Open').count()
    in_progress_tickets = queryset.filter(status='In_Progress').count()
    resolved_tickets = queryset.filter(status='Resolved').count()
    closed_tickets = queryset.filter(status='Closed').count()
    
    # Overdue tickets
    overdue_tickets = queryset.filter(
        sla_due_date__lt=timezone.now(),
        status__in=['Open', 'Assigned', 'In_Progress']
    ).count()
    
    # Tickets by priority
    priority_stats = {}
    for priority in ['Low', 'Medium', 'High', 'Critical']:
        priority_stats[priority.lower()] = queryset.filter(priority=priority).count()
    
    # Tickets by status
    status_stats = {
        'open': open_tickets,
        'assigned': queryset.filter(status='Assigned').count(),
        'in_progress': in_progress_tickets,
        'resolved': resolved_tickets,
        'closed': closed_tickets,
    }
    
    # Recent activity (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_tickets = queryset.filter(created_at__gte=seven_days_ago)
    recent_resolved = queryset.filter(
        resolved_date__gte=seven_days_ago
    ).count()
    
    # Average resolution time (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    resolved_tickets_30_days = queryset.filter(
        resolved_date__gte=thirty_days_ago,
        created_at__gte=thirty_days_ago
    )

    avg_resolution_time = None
    if resolved_tickets_30_days.exists():
        total_resolution_time = sum(
            (ticket.resolved_date - ticket.created_at).total_seconds() / 3600
            for ticket in resolved_tickets_30_days
            if ticket.resolved_date
        )
        avg_resolution_time = total_resolution_time / resolved_tickets_30_days.count()

    # SLA compliance rate
    sla_compliant = queryset.filter(
        status__in=['Resolved', 'Closed'],
        resolved_date__lte=F('sla_due_date')
    ).count()
    
    total_resolved_closed = queryset.filter(
        status__in=['Resolved', 'Closed']
    ).count()
    
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
        }
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mission_statistics(request):
    """Get statistics by mission (HQ Super Admin only)"""
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
                sla_due_date__lt=timezone.now(),
                status__in=['Open', 'Assigned', 'In_Progress']
            ).count(),
        }
        
        mission_stats.append(stats)
    
    return Response(mission_stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ticket_trends(request):
    """Get ticket creation trends over time"""
    queryset = Ticket.objects.all()
    
    # Mission isolation for non-HQ users
    if request.user.role != 'HQ_Super_Admin':
        queryset = queryset.filter(mission=request.user.mission)
    
    # Role-based filtering
    if request.user.role == 'Requester':
        queryset = queryset.filter(requester=request.user)
    elif request.user.role == 'Agent':
        queryset = queryset.filter(
            Q(assigned_agent=request.user) | Q(status='Open')
        )
    
    # Get last 30 days of data
    thirty_days_ago = timezone.now() - timedelta(days=30)
    queryset = queryset.filter(created_at__gte=thirty_days_ago)
    
    # Group by date
    from django.db.models import TruncDate
    trends = queryset.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    return Response(list(trends))


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def agent_performance(request):
    """Get agent performance statistics"""
    if request.user.role not in ['Mission_Admin', 'HQ_Super_Admin']:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    queryset = User.objects.filter(role='Agent')
    
    # Mission isolation for Mission Admin
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
                sla_due_date__lt=timezone.now(),
                status__in=['Assigned', 'In_Progress']
            ).count(),
        }
        
        # Average resolution time
        resolved_tickets = agent_tickets.filter(status='Resolved')
        if resolved_tickets.exists():
            total_resolution_time = sum(
                (ticket.resolved_date - ticket.created_at).total_seconds() / 3600
                for ticket in resolved_tickets
            )
            stats['average_resolution_hours'] = round(
                total_resolution_time / resolved_tickets.count(), 2
            )
        else:
            stats['average_resolution_hours'] = None
        
        agent_stats.append(stats)
    
    return Response(agent_stats)
