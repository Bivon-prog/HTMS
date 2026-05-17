"""Auto-escalate overdue open tickets to HQ (pdf2 automatic Tier-2 escalation)."""
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.authentication.models import User
from apps.tickets.models import AuditLog, Ticket
from apps.tickets.working_hours import recalculate_ticket_sla


def _system_actor():
    return User.objects.filter(role__in=['HQ_Super_Admin', 'Mission_Admin']).order_by('id').first()


class Command(BaseCommand):
    help = 'Mark overdue tickets as escalated_to_hq and reset SLA on Nairobi HQ calendar.'

    def handle(self, *args, **options):
        actor = _system_actor()
        if not actor:
            self.stderr.write(self.style.ERROR('No HQ/Mission admin user found — cannot write audit rows.'))
            return

        now = timezone.now()
        qs = Ticket.objects.filter(
            escalated_to_hq=False,
            sla_due_date__isnull=False,
            sla_due_date__lt=now,
            status__in=['Open', 'Assigned', 'In_Progress'],
        )
        n = 0
        for ticket in qs.iterator():
            ticket.escalated_to_hq = True
            ticket.escalation_reason = 'Automatic escalation: SLA due time passed (system job).'
            recalculate_ticket_sla(ticket, from_time=now)
            ticket.save(update_fields=['escalated_to_hq', 'escalation_reason', 'sla_due_date', 'updated_at'])
            AuditLog.objects.create(
                user=actor,
                action='Escalated',
                entity_type='ticket',
                entity_id=str(ticket.id),
                new_values={'automatic': True},
                ip_address=None,
            )
            n += 1
        self.stdout.write(self.style.SUCCESS(f'Escalated {n} ticket(s) to HQ.'))
