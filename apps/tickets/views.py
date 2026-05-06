from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.utils import timezone
from .models import Ticket, TicketComment, TicketAttachment, AuditLog
from .serializers import (
    TicketSerializer, TicketCreateSerializer, TicketStatusUpdateSerializer,
    TicketAssignmentSerializer, TicketCommentSerializer, TicketAttachmentSerializer,
    AuditLogSerializer,
)
from apps.permissions import IsMissionUserOrAdmin, CanAssignTickets


class TicketListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'mission']
    search_fields = ['title', 'description', 'ticket_number']
    ordering_fields = ['created_at', 'sla_due_date', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Ticket.objects.select_related(
            'requester', 'assigned_agent', 'category', 'mission'
        ).prefetch_related('comments', 'attachments')

        user = self.request.user

        # Mission isolation
        if user.role != 'HQ_Super_Admin':
            qs = qs.filter(mission=user.mission)

        # Role-based visibility
        if user.role == 'Requester':
            qs = qs.filter(requester=user)
        elif user.role == 'Agent':
            # Agents see their assigned tickets + all open tickets in their mission
            qs = qs.filter(Q(assigned_agent=user) | Q(status='Open'))

        return qs

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
        qs = Ticket.objects.select_related(
            'requester', 'assigned_agent', 'category', 'mission'
        ).prefetch_related('comments', 'attachments')

        user = self.request.user
        if user.role != 'HQ_Super_Admin':
            qs = qs.filter(mission=user.mission)
        if user.role == 'Requester':
            qs = qs.filter(requester=user)
        return qs


class TicketStatusUpdateView(generics.UpdateAPIView):
    serializer_class = TicketStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, CanAssignTickets]

    def get_queryset(self):
        qs = Ticket.objects.all()
        if self.request.user.role != 'HQ_Super_Admin':
            qs = qs.filter(mission=self.request.user.mission)
        return qs


class TicketAssignmentView(generics.UpdateAPIView):
    serializer_class = TicketAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, CanAssignTickets]

    def get_queryset(self):
        qs = Ticket.objects.all()
        if self.request.user.role != 'HQ_Super_Admin':
            qs = qs.filter(mission=self.request.user.mission)
        return qs


class TicketCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _get_ticket(self):
        ticket_id = self.kwargs['ticket_id']
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound('Ticket not found')
        user = self.request.user
        if user.role != 'HQ_Super_Admin' and ticket.mission != user.mission:
            raise PermissionDenied('Cannot access tickets from other missions')
        return ticket

    def get_queryset(self):
        ticket = self._get_ticket()
        qs = TicketComment.objects.filter(ticket=ticket).select_related('author').prefetch_related('attachments')
        # Requesters only see public comments
        if self.request.user.role == 'Requester':
            qs = qs.filter(is_internal=False)
        return qs

    def perform_create(self, serializer):
        ticket = self._get_ticket()
        is_internal = serializer.validated_data.get('is_internal', False)
        # Requesters cannot post internal notes
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
            from rest_framework.exceptions import NotFound
            raise NotFound('Ticket not found')
        user = self.request.user
        if user.role != 'HQ_Super_Admin' and ticket.mission != user.mission:
            raise PermissionDenied('Cannot access tickets from other missions')
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

        # Enforce max 5 attachments per ticket
        if TicketAttachment.objects.filter(ticket=ticket).count() >= 5:
            raise ValidationError('Maximum 5 attachments per ticket')

        serializer.save(
            ticket=ticket,
            uploaded_by=self.request.user,
            filename=file.name,
            mime_type=file.content_type,
            file_size_bytes=file.size,
        )


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
                mission=user.mission
            ).values_list('id', flat=True)
            qs = qs.filter(
                Q(entity_type='ticket', entity_id__in=mission_ticket_ids) |
                Q(user__mission=user.mission)
            )
        return qs


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ticket_statistics(request):
    """Ticket statistics for dashboard widgets."""
    qs = Ticket.objects.all()
    user = request.user

    if user.role != 'HQ_Super_Admin':
        qs = qs.filter(mission=user.mission)
    if user.role == 'Requester':
        qs = qs.filter(requester=user)
    elif user.role == 'Agent':
        qs = qs.filter(Q(assigned_agent=user) | Q(status='Open'))

    stats = {
        'total':       qs.count(),
        'open':        qs.filter(status='Open').count(),
        'assigned':    qs.filter(status='Assigned').count(),
        'in_progress': qs.filter(status='In_Progress').count(),
        'resolved':    qs.filter(status='Resolved').count(),
        'closed':      qs.filter(status='Closed').count(),
        'overdue':     qs.filter(
            sla_due_date__lt=timezone.now(),
            status__in=['Open', 'Assigned', 'In_Progress']
        ).count(),
        'by_priority': {
            'low':      qs.filter(priority='Low').count(),
            'medium':   qs.filter(priority='Medium').count(),
            'high':     qs.filter(priority='High').count(),
            'critical': qs.filter(priority='Critical').count(),
        },
    }
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def escalate_ticket(request, ticket_id):
    """Escalate a ticket to HQ."""
    if request.user.role not in ['Agent', 'Mission_Admin', 'HQ_Super_Admin']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role != 'HQ_Super_Admin' and ticket.mission != request.user.mission:
        return Response({'error': 'Cannot access tickets from other missions'}, status=status.HTTP_403_FORBIDDEN)

    reason = request.data.get('reason', '').strip()
    if not reason:
        return Response({'error': 'Reason is required for escalation'}, status=status.HTTP_400_BAD_REQUEST)

    ticket.escalated_to_hq = True
    ticket.escalation_reason = reason
    ticket.save(update_fields=['escalated_to_hq', 'escalation_reason', 'updated_at'])

    AuditLog.objects.create(
        user=request.user,
        action='Escalated',
        entity_type='ticket',
        entity_id=ticket.id,
        new_values={'escalated_to_hq': True, 'escalation_reason': reason},
        ip_address=request.META.get('REMOTE_ADDR'),
    )

    return Response({'message': 'Ticket escalated to HQ successfully'})
