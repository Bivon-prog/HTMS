import csv
from io import StringIO

from django.db.models import Q
from django.http import FileResponse, Http404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.permissions import CanAssignTickets, IsHQSuperAdmin, IsMissionUserOrAdmin

from .access import ticket_list_for_user, user_can_access_ticket
from .models import AuditLog, Ticket, TicketAttachment, TicketComment
from .serializers import (
    AuditLogSerializer,
    TicketAssignmentSerializer,
    TicketAttachmentSerializer,
    TicketCommentSerializer,
    TicketCreateSerializer,
    TicketSerializer,
    TicketStatusUpdateSerializer,
)


class TicketListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'mission', 'assigned_agent']
    search_fields = ['title', 'description', 'ticket_number']
    ordering_fields = ['created_at', 'sla_due_date', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        return ticket_list_for_user(self.request.user)

    def get_serializer_class(self):
        return TicketCreateSerializer if self.request.method == 'POST' else TicketSerializer

    def perform_create(self, serializer):
        serializer.save()


class TicketDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsMissionUserOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TicketStatusUpdateSerializer
        return TicketSerializer

    def get_queryset(self):
        return ticket_list_for_user(self.request.user)


class TicketStatusUpdateView(generics.UpdateAPIView):
    serializer_class = TicketStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, CanAssignTickets]

    def get_queryset(self):
        return ticket_list_for_user(self.request.user)


class TicketAssignmentView(generics.UpdateAPIView):
    serializer_class = TicketAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, CanAssignTickets]

    def get_queryset(self):
        return ticket_list_for_user(self.request.user)


class TicketCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _get_ticket(self):
        ticket_id = self.kwargs['ticket_id']
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            raise NotFound('Ticket not found')
        if not user_can_access_ticket(self.request.user, ticket):
            raise PermissionDenied('Cannot access this ticket')
        return ticket

    def get_queryset(self):
        ticket = self._get_ticket()
        qs = TicketComment.objects.filter(ticket=ticket).select_related('author').prefetch_related('attachments')
        if self.request.user.role == 'Requester':
            qs = qs.filter(is_internal=False)
        return qs

    def perform_create(self, serializer):
        ticket = self._get_ticket()
        is_internal = serializer.validated_data.get('is_internal', False)
        if self.request.user.role == 'Requester':
            is_internal = False
        serializer.save(ticket=ticket, author=self.request.user, is_internal=is_internal)


class TicketAttachmentListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _get_ticket(self):
        ticket_id = self.kwargs['ticket_id']
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            raise NotFound('Ticket not found')
        if not user_can_access_ticket(self.request.user, ticket):
            raise PermissionDenied('Cannot access this ticket')
        return ticket

    def get_queryset(self):
        ticket = self._get_ticket()
        return TicketAttachment.objects.filter(ticket=ticket).select_related('uploaded_by')

    def perform_create(self, serializer):
        ticket = self._get_ticket()
        file = self.request.FILES.get('file')
        if not file:
            raise ValidationError('No file provided')

        if file.size > 10 * 1024 * 1024:
            raise ValidationError('File size cannot exceed 10MB')

        allowed_types = [
            'application/pdf',
            'image/jpeg',
            'image/png',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        ]
        if file.content_type not in allowed_types:
            raise ValidationError('Invalid file type. Only PDF, JPEG, PNG, and DOCX are allowed')

        if TicketAttachment.objects.filter(ticket=ticket).count() >= 5:
            raise ValidationError('Maximum 5 attachments per ticket')

        serializer.save(
            ticket=ticket,
            uploaded_by=self.request.user,
            filename=file.name,
            mime_type=file.content_type,
            file_size_bytes=file.size,
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ticket_attachment_download(request, ticket_id, pk):
    """Authenticated download (SRS 4.4 — avoids public MEDIA URLs)."""
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404()
    if not user_can_access_ticket(request.user, ticket):
        raise PermissionDenied()

    try:
        att = TicketAttachment.objects.get(id=pk, ticket=ticket)
    except TicketAttachment.DoesNotExist:
        raise Http404()

    if not att.file:
        raise Http404()
    return FileResponse(att.file.open('rb'), as_attachment=True, filename=att.filename)


class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        qs = AuditLog.objects.select_related('user')

        if ticket_id:
            qs = qs.filter(entity_type='ticket', entity_id=ticket_id)

        user = self.request.user
        if user.role != 'HQ_Super_Admin':
            mission_ticket_ids = Ticket.objects.filter(
                mission=user.mission,
            ).values_list('id', flat=True)
            qs = qs.filter(
                Q(entity_type='ticket', entity_id__in=list(mission_ticket_ids))
                | Q(user__mission=user.mission),
            )
        return qs


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsHQSuperAdmin])
def export_audit_logs_csv(request):
    """Bulk audit export for HQ Super Admin (SRS 3.6)."""
    buf = StringIO()
    w = csv.writer(buf)
    w.writerow(['id', 'action', 'entity_type', 'entity_id', 'user_email', 'ip_address', 'created_at'])
    for row in AuditLog.objects.select_related('user').iterator():
        w.writerow([
            row.id, row.action, row.entity_type, row.entity_id,
            row.user.email if row.user_id else '',
            row.ip_address or '', row.created_at.isoformat(),
        ])
    from django.http import HttpResponse

    resp = HttpResponse(buf.getvalue(), content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="audit_logs.csv"'
    return resp


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsHQSuperAdmin])
def export_tickets_csv(request):
    """Mission / global ticket export as CSV (SRS 3.9 reports — CSV path)."""
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
    from django.http import HttpResponse

    resp = HttpResponse(buf.getvalue(), content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="tickets_export.csv"'
    return resp


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ticket_statistics(request):
    qs = ticket_list_for_user(request.user)

    stats = {
        'total': qs.count(),
        'open': qs.filter(status='Open').count(),
        'assigned': qs.filter(status='Assigned').count(),
        'in_progress': qs.filter(status='In_Progress').count(),
        'resolved': qs.filter(status='Resolved').count(),
        'closed': qs.filter(status='Closed').count(),
        'overdue': qs.filter(
            sla_due_date__isnull=False,
            sla_due_date__lt=timezone.now(),
            status__in=['Open', 'Assigned', 'In_Progress'],
        ).count(),
        'by_priority': {
            'low': qs.filter(priority='Low').count(),
            'medium': qs.filter(priority='Medium').count(),
            'high': qs.filter(priority='High').count(),
            'critical': qs.filter(priority='Critical').count(),
        },
    }
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def escalate_ticket(request, ticket_id):
    if request.user.role not in ['Agent', 'Mission_Admin', 'HQ_Super_Admin']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

    if not user_can_access_ticket(request.user, ticket):
        return Response({'error': 'Cannot access this ticket'}, status=status.HTTP_403_FORBIDDEN)

    reason = request.data.get('reason', '').strip()
    if not reason:
        return Response({'error': 'Reason is required for escalation'}, status=status.HTTP_400_BAD_REQUEST)

    from apps.tickets.working_hours import recalculate_ticket_sla

    ticket.escalated_to_hq = True
    ticket.escalation_reason = reason
    recalculate_ticket_sla(ticket, from_time=timezone.now())
    ticket.save(update_fields=['escalated_to_hq', 'escalation_reason', 'sla_due_date', 'updated_at'])

    AuditLog.objects.create(
        user=request.user,
        action='Escalated',
        entity_type='ticket',
        entity_id=str(ticket.id),
        new_values={'escalated_to_hq': True, 'escalation_reason': reason},
        ip_address=request.META.get('REMOTE_ADDR'),
    )

    return Response({'message': 'Ticket escalated to HQ successfully'})
