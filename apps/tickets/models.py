from django.db import models
from django.utils import timezone
from django.conf import settings
from apps.authentication.models import User
from apps.missions.models import Mission, TicketCategory


def generate_ticket_number():
    """Generate unique ticket number in format HTMS-YYYY-NNNNN"""
    import datetime
    year = datetime.datetime.now().year
    prefix = f"HTMS-{year}-"
    
    # Get the highest sequence number for this year
    last_ticket = Ticket.objects.filter(
        ticket_number__startswith=prefix
    ).order_by('-ticket_number').first()
    
    if last_ticket:
        last_sequence = int(last_ticket.ticket_number.split('-')[-1])
        new_sequence = last_sequence + 1
    else:
        new_sequence = 1
    
    return f"{prefix}{new_sequence:05d}"


class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Assigned', 'Assigned'),
        ('In_Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    ticket_number = models.CharField(max_length=20, unique=True, default=generate_ticket_number)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    category = models.ForeignKey(TicketCategory, on_delete=models.PROTECT, related_name='tickets')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='requested_tickets',
        help_text='Staff member who submitted the ticket (assistant when using OBO)',
    )
    beneficiary = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='beneficiary_tickets',
        help_text='Senior official on whose behalf the ticket was raised (SRS 4.6 OBO)',
    )
    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tickets'
    )
    
    mission = models.ForeignKey(Mission, on_delete=models.PROTECT, related_name='tickets')
    linked_asset = models.ForeignKey('assets.Asset', on_delete=models.SET_NULL, null=True, blank=True)
    
    escalated_to_hq = models.BooleanField(default=False)
    escalation_reason = models.TextField(blank=True)
    
    sla_due_date = models.DateTimeField(null=True, blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tickets'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ticket_number} - {self.title}"

    def save(self, *args, **kwargs):
        # Auto-set dates based on status changes
        if self.pk:
            old_ticket = Ticket.objects.get(pk=self.pk)
            
            # Set resolved_date when status changes to Resolved
            if old_ticket.status != 'Resolved' and self.status == 'Resolved':
                self.resolved_date = timezone.now()
            
            # Set closed_date when status changes to Closed
            if old_ticket.status != 'Closed' and self.status == 'Closed':
                self.closed_date = timezone.now()
        
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Check if ticket is overdue based on SLA"""
        if self.sla_due_date and self.status not in ['Resolved', 'Closed']:
            from django.utils import timezone
            return timezone.now() > self.sla_due_date
        return False


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='ticket_comments'
    )
    content = models.TextField()
    is_internal = models.BooleanField(default=False)  # Internal notes vs public comments
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_comments'
        verbose_name = 'Ticket Comment'
        verbose_name_plural = 'Ticket Comments'
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.get_full_name()} on {self.ticket.ticket_number}"


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    comment = models.ForeignKey(
        TicketComment, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='attachments'
    )
    
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='ticket_attachments/')
    mime_type = models.CharField(max_length=100)
    file_size_bytes = models.IntegerField()
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='uploaded_attachments'
    )
    
    virus_scanned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_attachments'
        verbose_name = 'Ticket Attachment'
        verbose_name_plural = 'Ticket Attachments'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.filename} - {self.ticket.ticket_number}"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('Created', 'Created'),
        ('Assigned', 'Assigned'),
        ('Status Changed', 'Status Changed'),
        ('Comment Added', 'Comment Added'),
        ('Reassigned', 'Reassigned'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
        ('Escalated', 'Escalated'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='audit_logs'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=50)  # 'ticket', 'user', 'mission', etc.
    entity_id = models.CharField(max_length=64)  # supports both int IDs and MongoDB ObjectId strings
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} on {self.entity_type} by {self.user.get_full_name()}"
