"""
Management command to load all 70 Kenyan diplomatic missions.
Usage: python manage_supabase.py load_missions
"""
from django.core.management.base import BaseCommand
from apps.missions.models import Mission, TicketCategory


MISSIONS = [
    # ── Africa ──────────────────────────────────────────────────────────────
    {"name": "Kenya Embassy Algiers",        "country": "Algeria",       "city": "Algiers",       "region": "Africa",      "timezone": "Africa/Algiers",      "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Luanda",         "country": "Angola",        "city": "Luanda",        "region": "Africa",      "timezone": "Africa/Luanda",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Gaborone","country": "Botswana",     "city": "Gaborone",      "region": "Africa",      "timezone": "Africa/Gaborone",     "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Bujumbura",      "country": "Burundi",       "city": "Bujumbura",     "region": "Africa",      "timezone": "Africa/Bujumbura",    "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Kinshasa",       "country": "DR Congo",      "city": "Kinshasa",      "region": "Africa",      "timezone": "Africa/Kinshasa",     "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Consulate Goma",         "country": "DR Congo",      "city": "Goma",          "region": "Africa",      "timezone": "Africa/Lubumbashi",   "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Djibouti",       "country": "Djibouti",      "city": "Djibouti",      "region": "Africa",      "timezone": "Africa/Djibouti",     "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Cairo",          "country": "Egypt",         "city": "Cairo",         "region": "Africa",      "timezone": "Africa/Cairo",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Accra",  "country": "Ghana",         "city": "Accra",         "region": "Africa",      "timezone": "Africa/Accra",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Addis Ababa",    "country": "Ethiopia",      "city": "Addis Ababa",   "region": "Africa",      "timezone": "Africa/Addis_Ababa",  "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Mission to AU/UNECA",    "country": "Ethiopia",      "city": "Addis Ababa",   "region": "Multilateral","timezone": "Africa/Addis_Ababa",  "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Abidjan",        "country": "Ivory Coast",   "city": "Abidjan",       "region": "Africa",      "timezone": "Africa/Abidjan",      "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Rabat",          "country": "Morocco",       "city": "Rabat",         "region": "Africa",      "timezone": "Africa/Casablanca",   "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Maputo",         "country": "Mozambique",    "city": "Maputo",        "region": "Africa",      "timezone": "Africa/Maputo",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Windhoek","country": "Namibia",      "city": "Windhoek",      "region": "Africa",      "timezone": "Africa/Windhoek",     "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Lagos",  "country": "Nigeria",       "city": "Lagos",         "region": "Africa",      "timezone": "Africa/Lagos",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Kigali", "country": "Rwanda",        "city": "Kigali",        "region": "Africa",      "timezone": "Africa/Kigali",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Dakar",          "country": "Senegal",       "city": "Dakar",         "region": "Africa",      "timezone": "Africa/Dakar",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Mogadishu",      "country": "Somalia",       "city": "Mogadishu",     "region": "Africa",      "timezone": "Africa/Mogadishu",    "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Consulate Hargeisa",     "country": "Somalia",       "city": "Hargeisa",      "region": "Africa",      "timezone": "Africa/Mogadishu",    "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Juba",           "country": "South Sudan",   "city": "Juba",          "region": "Africa",      "timezone": "Africa/Juba",         "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Pretoria","country": "South Africa", "city": "Pretoria",      "region": "Africa",      "timezone": "Africa/Johannesburg", "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Khartoum",       "country": "Sudan",         "city": "Khartoum",      "region": "Africa",      "timezone": "Africa/Khartoum",     "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Dar es Salaam","country": "Tanzania","city": "Dar es Salaam", "region": "Africa",      "timezone": "Africa/Dar_es_Salaam","working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Consulate Arusha",       "country": "Tanzania",      "city": "Arusha",        "region": "Africa",      "timezone": "Africa/Dar_es_Salaam","working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Tunis",          "country": "Tunisia",       "city": "Tunis",         "region": "Africa",      "timezone": "Africa/Tunis",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Kampala","country": "Uganda",        "city": "Kampala",       "region": "Africa",      "timezone": "Africa/Kampala",      "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Lusaka", "country": "Zambia",        "city": "Lusaka",        "region": "Africa",      "timezone": "Africa/Lusaka",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Harare",         "country": "Zimbabwe",      "city": "Harare",        "region": "Africa",      "timezone": "Africa/Harare",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},

    # ── Asia & Oceania ───────────────────────────────────────────────────────
    {"name": "Kenya High Commission Canberra","country": "Australia",    "city": "Canberra",      "region": "Asia",        "timezone": "Australia/Sydney",    "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Beijing",        "country": "China",         "city": "Beijing",       "region": "Asia",        "timezone": "Asia/Shanghai",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Consulate Guangzhou",    "country": "China",         "city": "Guangzhou",     "region": "Asia",        "timezone": "Asia/Shanghai",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya High Commission New Delhi","country": "India",       "city": "New Delhi",     "region": "Asia",        "timezone": "Asia/Kolkata",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
    {"name": "Kenya Embassy Jakarta",        "country": "Indonesia",     "city": "Jakarta",       "region": "Asia",        "timezone": "Asia/Jakarta",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "16:00"},
    {"name": "Kenya Embassy Tokyo",          "country": "Japan",         "city": "Tokyo",         "region": "Asia",        "timezone": "Asia/Tokyo",          "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
    {"name": "Kenya High Commission Kuala Lumpur","country": "Malaysia", "city": "Kuala Lumpur",  "region": "Asia",        "timezone": "Asia/Kuala_Lumpur",   "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:30", "work_end_time": "17:00"},
    {"name": "Kenya High Commission Wellington","country": "New Zealand","city": "Wellington",    "region": "Asia",        "timezone": "Pacific/Auckland",    "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Islamabad",      "country": "Pakistan",      "city": "Islamabad",     "region": "Asia",        "timezone": "Asia/Karachi",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Seoul",          "country": "South Korea",   "city": "Seoul",         "region": "Asia",        "timezone": "Asia/Seoul",          "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "18:00"},
    {"name": "Kenya Embassy Bangkok",        "country": "Thailand",      "city": "Bangkok",       "region": "Asia",        "timezone": "Asia/Bangkok",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:30", "work_end_time": "16:30"},

    # ── Europe ───────────────────────────────────────────────────────────────
    {"name": "Kenya Embassy Vienna",         "country": "Austria",       "city": "Vienna",        "region": "Europe",      "timezone": "Europe/Vienna",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Brussels",       "country": "Belgium",       "city": "Brussels",      "region": "Europe",      "timezone": "Europe/Brussels",     "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Paris",          "country": "France",        "city": "Paris",         "region": "Europe",      "timezone": "Europe/Paris",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
    {"name": "Kenya Embassy Berlin",         "country": "Germany",       "city": "Berlin",        "region": "Europe",      "timezone": "Europe/Berlin",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Athens",         "country": "Greece",        "city": "Athens",        "region": "Europe",      "timezone": "Europe/Athens",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Dublin",         "country": "Ireland",       "city": "Dublin",        "region": "Europe",      "timezone": "Europe/Dublin",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
    {"name": "Kenya Embassy Rome",           "country": "Italy",         "city": "Rome",          "region": "Europe",      "timezone": "Europe/Rome",         "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy The Hague",      "country": "Netherlands",   "city": "The Hague",     "region": "Europe",      "timezone": "Europe/Amsterdam",    "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Moscow",         "country": "Russia",        "city": "Moscow",        "region": "Europe",      "timezone": "Europe/Moscow",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "18:00"},
    {"name": "Kenya Embassy Madrid",         "country": "Spain",         "city": "Madrid",        "region": "Europe",      "timezone": "Europe/Madrid",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Stockholm",      "country": "Sweden",        "city": "Stockholm",     "region": "Europe",      "timezone": "Europe/Stockholm",    "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Permanent Mission Geneva","country": "Switzerland",  "city": "Geneva",        "region": "Multilateral","timezone": "Europe/Zurich",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
    {"name": "Kenya High Commission London", "country": "United Kingdom","city": "London",        "region": "Europe",      "timezone": "Europe/London",       "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},

    # ── Middle East ──────────────────────────────────────────────────────────
    {"name": "Kenya Embassy Tehran",         "country": "Iran",          "city": "Tehran",        "region": "Middle_East", "timezone": "Asia/Tehran",         "working_week_start": 7, "working_week_end": 4, "work_start_time": "08:00", "work_end_time": "16:00"},
    {"name": "Kenya Embassy Tel Aviv",       "country": "Israel",        "city": "Tel Aviv",      "region": "Middle_East", "timezone": "Asia/Jerusalem",      "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "16:00"},
    {"name": "Kenya Embassy Amman",          "country": "Jordan",        "city": "Amman",         "region": "Middle_East", "timezone": "Asia/Amman",          "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "16:00"},
    {"name": "Kenya Embassy Kuwait City",    "country": "Kuwait",        "city": "Kuwait City",   "region": "Middle_East", "timezone": "Asia/Kuwait",         "working_week_start": 7, "working_week_end": 4, "work_start_time": "08:00", "work_end_time": "16:00"},
    {"name": "Kenya Embassy Muscat",         "country": "Oman",          "city": "Muscat",        "region": "Middle_East", "timezone": "Asia/Muscat",         "working_week_start": 7, "working_week_end": 4, "work_start_time": "07:30", "work_end_time": "14:30"},
    {"name": "Kenya Embassy Doha",           "country": "Qatar",         "city": "Doha",          "region": "Middle_East", "timezone": "Asia/Qatar",          "working_week_start": 7, "working_week_end": 4, "work_start_time": "07:00", "work_end_time": "15:00"},
    {"name": "Kenya Embassy Riyadh",         "country": "Saudi Arabia",  "city": "Riyadh",        "region": "Middle_East", "timezone": "Asia/Riyadh",         "working_week_start": 7, "working_week_end": 4, "work_start_time": "08:00", "work_end_time": "16:00"},
    {"name": "Kenya Consulate Jeddah",       "country": "Saudi Arabia",  "city": "Jeddah",        "region": "Middle_East", "timezone": "Asia/Riyadh",         "working_week_start": 7, "working_week_end": 4, "work_start_time": "08:00", "work_end_time": "16:00"},
    {"name": "Kenya Consulate Dubai",        "country": "UAE",           "city": "Dubai",         "region": "Middle_East", "timezone": "Asia/Dubai",          "working_week_start": 7, "working_week_end": 4, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Abu Dhabi",      "country": "UAE",           "city": "Abu Dhabi",     "region": "Middle_East", "timezone": "Asia/Dubai",          "working_week_start": 7, "working_week_end": 4, "work_start_time": "08:00", "work_end_time": "17:00"},

    # ── Americas ─────────────────────────────────────────────────────────────
    {"name": "Kenya High Commission Ottawa", "country": "Canada",        "city": "Ottawa",        "region": "Americas",    "timezone": "America/Toronto",     "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Washington D.C.","country": "USA",           "city": "Washington D.C.","region": "Americas",   "timezone": "America/New_York",    "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
    {"name": "Kenya Permanent Mission New York","country": "USA",        "city": "New York",      "region": "Multilateral","timezone": "America/New_York",    "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
    {"name": "Kenya Consulate Los Angeles",  "country": "USA",           "city": "Los Angeles",   "region": "Americas",    "timezone": "America/Los_Angeles", "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},
    {"name": "Kenya Embassy Havana",         "country": "Cuba",          "city": "Havana",        "region": "Americas",    "timezone": "America/Havana",      "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:30", "work_end_time": "16:30"},
    {"name": "Kenya Embassy Brasilia",       "country": "Brazil",        "city": "Brasilia",      "region": "Americas",    "timezone": "America/Sao_Paulo",   "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:00"},

    # ── Multilateral ─────────────────────────────────────────────────────────
    {"name": "Kenya Permanent Mission to UN Nairobi","country": "Kenya", "city": "Nairobi",       "region": "Multilateral","timezone": "Africa/Nairobi",      "working_week_start": 1, "working_week_end": 5, "work_start_time": "08:00", "work_end_time": "17:00"},
    {"name": "Kenya Permanent Mission to UN New York","country": "USA",  "city": "New York",      "region": "Multilateral","timezone": "America/New_York",    "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
    {"name": "Kenya Permanent Delegation to UNESCO Paris","country": "France","city": "Paris",    "region": "Multilateral","timezone": "Europe/Paris",        "working_week_start": 1, "working_week_end": 5, "work_start_time": "09:00", "work_end_time": "17:30"},
]

TICKET_CATEGORIES = [
    {"name": "IT",         "description": "Information Technology issues — hardware, software, network, email, accounts", "auto_escalation_hours": 48},
    {"name": "HR",         "description": "Human Resources matters — leave, payroll, contracts, staff welfare",           "auto_escalation_hours": 72},
    {"name": "Facilities", "description": "Facilities and maintenance — office equipment, building, utilities",           "auto_escalation_hours": 72},
    {"name": "Finance",    "description": "Finance and procurement matters",                                              "auto_escalation_hours": 96},
    {"name": "Security",   "description": "Security and access control issues",                                           "auto_escalation_hours": 4},
    {"name": "Other",      "description": "General enquiries and other issues",                                           "auto_escalation_hours": 96},
]


class Command(BaseCommand):
    help = 'Load all 70 Kenyan diplomatic missions and ticket categories'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing missions before loading')

    def handle(self, *args, **options):
        if options['clear']:
            Mission.objects.all().delete()
            TicketCategory.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing missions and categories.'))

        # Load ticket categories
        created_cats = 0
        for cat_data in TICKET_CATEGORIES:
            _, created = TicketCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'auto_escalation_hours': cat_data['auto_escalation_hours'],
                }
            )
            if created:
                created_cats += 1

        self.stdout.write(self.style.SUCCESS(f'✓ {created_cats} ticket categories loaded (skipped existing)'))

        # Load missions
        created_missions = 0
        skipped = 0
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
                }
            )
            if created:
                created_missions += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ {created_missions} missions loaded, {skipped} already existed.\n'
                f'  Total missions in DB: {Mission.objects.count()}'
            )
        )
