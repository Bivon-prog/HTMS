"""In-app + email notifications respecting user preferences (SRS 3.7)."""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from apps.notifications.models import Notification, NotificationPreference

logger = logging.getLogger(__name__)


def _pref_allows(user, event_type: str, channel: str) -> bool:
    pref = NotificationPreference.objects.filter(user=user, event_type=event_type).first()
    if not pref:
        return True
    if channel == 'email':
        return pref.email_enabled
    return pref.in_app_enabled


def notify_users(event_type: str, users, message: str, *, entity_type: str, entity_id: int):
    """Create in-app notifications and optionally send email."""
    for user in users:
        if not user or not user.is_active:
            continue
        if _pref_allows(user, event_type, 'in_app'):
            Notification.objects.create(
                user=user,
                event_type=event_type,
                message=message,
                entity_type=entity_type,
                entity_id=entity_id,
            )
        if _pref_allows(user, event_type, 'email') and getattr(settings, 'EMAIL_HOST', ''):
            try:
                send_mail(
                    subject=f'HTMS: {event_type.replace("_", " ").title()}',
                    message=message,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@htms.local'),
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning('Email notify failed for %s: %s', user.email, exc)


def notify_ticket_routing(ticket):
    """Notify mission admins + departmental agents when a ticket is created."""
    from apps.authentication.models import User

    event = 'ticket_created'
    msg = f'New ticket {ticket.ticket_number}: {ticket.title}'
    recipients = User.objects.filter(mission=ticket.mission, is_active=True).filter(
        Q(role='Mission_Admin')
        | Q(role='Agent', department=ticket.category.routing_department)
    )
    notify_users(event, list(recipients), msg, entity_type='ticket', entity_id=str(ticket.id))
