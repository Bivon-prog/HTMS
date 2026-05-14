"""Auto-close tickets stuck in Resolved (SRS 3.3 — configurable calendar-day proxy for business days)."""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.authentication.models import User
from apps.tickets.models import AuditLog, Ticket


def _system_actor():
    return User.objects.filter(role__in=['HQ_Super_Admin', 'Mission_Admin']).order_by('id').first()


class Command(BaseCommand):
    help = 'Set status Closed for Resolved tickets older than --days (default 5 calendar days).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=5,
            help='Minimum days in Resolved before auto-closing.',
        )

    def handle(self, *args, **options):
        actor = _system_actor()
        if not actor:
            self.stderr.write(self.style.ERROR('No HQ/Mission admin user found — cannot write audit rows.'))
            return

        days = options['days']
        cutoff = timezone.now() - timedelta(days=days)
        qs = Ticket.objects.filter(status='Resolved', resolved_date__isnull=False, resolved_date__lt=cutoff)
        closed = 0
        for ticket in qs.iterator():
            ticket.status = 'Closed'
            ticket.save(update_fields=['status', 'closed_date', 'updated_at'])
            AuditLog.objects.create(
                user=actor,
                action='Closed',
                entity_type='ticket',
                entity_id=ticket.id,
                new_values={'auto_closed': True, 'reason': f'Resolved > {days} days without confirmation'},
                ip_address=None,
            )
            closed += 1
        self.stdout.write(self.style.SUCCESS(f'Auto-closed {closed} ticket(s).'))
