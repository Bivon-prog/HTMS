from django.db import models
from django.conf import settings


class Notification(models.Model):
    EVENT_TYPE_CHOICES = [
        ('ticket_created', 'Ticket Created'),
        ('ticket_assigned', 'Ticket Assigned'),
        ('ticket_status_changed', 'Ticket Status Changed'),
        ('ticket_comment_added', 'Ticket Comment Added'),
        ('ticket_resolved', 'Ticket Resolved'),
        ('ticket_escalated', 'Ticket Escalated'),
        ('sla_breach_warning', 'SLA Breach Warning'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    message = models.TextField()
    entity_type = models.CharField(max_length=50)  # 'ticket', 'user', etc.
    entity_id = models.IntegerField()  # ID of the related entity
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.get_full_name()}: {self.message[:50]}"


class NotificationPreference(models.Model):
    EVENT_TYPE_CHOICES = [
        ('ticket_created', 'Ticket Created'),
        ('ticket_assigned', 'Ticket Assigned'),
        ('ticket_status_changed', 'Ticket Status Changed'),
        ('ticket_comment_added', 'Ticket Comment Added'),
        ('ticket_resolved', 'Ticket Resolved'),
        ('ticket_escalated', 'Ticket Escalated'),
        ('sla_breach_warning', 'SLA Breach Warning'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    email_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
        unique_together = ['user', 'event_type']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_event_type_display()}"
