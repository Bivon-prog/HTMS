"""Seed missions and ticket categories (SRS: extend to full 70-mission registry as provided by the Ministry)."""
from django.core.management.base import BaseCommand

from apps.missions.models import Mission, TicketCategory


# Representative subset — replace/extend with the authoritative 70-mission list for production UAT.
MISSIONS = [
    {"name": "Kenya Permanent Mission to UN Nairobi", "country": "Kenya", "city": "Nairobi", "region": "Multilateral", "timezone": "Africa/Nairobi", "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission London", "country": "United Kingdom", "city": "London", "region": "Europe", "timezone": "Europe/London", "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
    {"name": "Kenya Embassy Washington D.C.", "country": "USA", "city": "Washington D.C.", "region": "Americas", "timezone": "America/New_York", "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
    {"name": "Kenya Embassy Riyadh", "country": "Saudi Arabia", "city": "Riyadh", "region": "Middle_East", "timezone": "Asia/Riyadh", "working_week_start": 7, "working_week_end": 4, "work_start_time": "08:00", "work_end_time": "16:00"},
    {"name": "Kenya Embassy Beijing", "country": "China", "city": "Beijing", "region": "Asia", "timezone": "Asia/Shanghai", "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Pretoria", "country": "South Africa", "city": "Pretoria", "region": "Africa", "timezone": "Africa/Johannesburg", "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
]

TICKET_CATEGORIES = [
    {"name": "IT", "routing_department": "IT", "description": "Information Technology issues", "auto_escalation_hours": 48},
    {"name": "HR", "routing_department": "HR", "description": "Human Resources matters", "auto_escalation_hours": 72},
    {"name": "Facilities", "routing_department": "Facilities", "description": "Facilities and maintenance", "auto_escalation_hours": 72},
    {"name": "Finance", "routing_department": "Finance", "description": "Finance and procurement", "auto_escalation_hours": 96},
    {"name": "Security", "routing_department": "IT", "description": "Security and access control", "auto_escalation_hours": 4},
    {"name": "Other", "routing_department": "Admin", "description": "General enquiries", "auto_escalation_hours": 96},
]


class Command(BaseCommand):
    help = 'Load missions and ticket categories'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear missions and categories first')

    def handle(self, *args, **options):
        if options['clear']:
            Mission.objects.all().delete()
            TicketCategory.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared missions and categories.'))

        for cat in TICKET_CATEGORIES:
            TicketCategory.objects.update_or_create(
                name=cat['name'],
                defaults={
                    'description': cat['description'],
                    'auto_escalation_hours': cat['auto_escalation_hours'],
                    'routing_department': cat['routing_department'],
                },
            )
        self.stdout.write(self.style.SUCCESS(f'Ticket categories: {TicketCategory.objects.count()}'))

        n = 0
        for m in MISSIONS:
            _, created = Mission.objects.get_or_create(
                name=m['name'],
                defaults={
                    'country': m['country'],
                    'city': m['city'],
                    'region': m['region'],
                    'timezone': m['timezone'],
                    'working_week_start': m['working_week_start'],
                    'working_week_end': m['working_week_end'],
                    'work_start_time': m['work_start_time'],
                    'work_end_time': m['work_end_time'],
                    'status': 'Active',
                },
            )
            if created:
                n += 1
        self.stdout.write(self.style.SUCCESS(f'Missions created: {n}; total missions: {Mission.objects.count()}'))
