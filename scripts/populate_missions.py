import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'htms.settings')
django.setup()

from apps.missions.models import Mission
import pytz

missions_data = {
    'Africa': [
        ('Algeria', 'Algiers'),
        ('Angola', 'Luanda'),
        ('Botswana', 'Gaborone'),
        ('Burundi', 'Bujumbura'),
        ('DR Congo', 'Kinshasa & Goma Consulate'),
        ('Djibouti', 'Djibouti City'),
        ('Egypt', 'Cairo'),
        ('Ethiopia', 'Addis Ababa'),
        ('Ghana', 'Accra'),
        ('Ivory Coast', 'Abidjan'),
        ('Morocco', 'Rabat'),
        ('Mozambique', 'Maputo'),
        ('Namibia', 'Windhoek'),
        ('Nigeria', 'Abuja'),
        ('Rwanda', 'Kigali'),
        ('Senegal', 'Dakar'),
        ('Somalia', 'Mogadishu & Hargeisa Liaison Office'),
        ('South Africa', 'Pretoria'),
        ('South Sudan', 'Juba'),
        ('Sudan', 'Khartoum'),
        ('Tanzania', 'Dar es Salaam & Arusha Consulate'),
        ('Uganda', 'Kampala'),
        ('Zambia', 'Lusaka'),
        ('Zimbabwe', 'Harare'),
    ],
    'Asia': [
        ('Australia', 'Canberra'),
        ('China', 'Beijing & Guangzhou Consulate'),
        ('India', 'New Delhi'),
        ('Indonesia', 'Jakarta'),
        ('Japan', 'Tokyo'),
        ('Malaysia', 'Kuala Lumpur'),
        ('Pakistan', 'Islamabad'),
        ('South Korea', 'Seoul'),
        ('Thailand', 'Bangkok'),
    ],
    'Europe': [
        ('Austria', 'Vienna'),
        ('Belgium', 'Brussels'),
        ('France', 'Paris'),
        ('Germany', 'Berlin'),
        ('Ireland', 'Dublin'),
        ('Italy', 'Rome'),
        ('Netherlands', 'The Hague'),
        ('Russia', 'Moscow'),
        ('Spain', 'Madrid'),
        ('Sweden', 'Stockholm'),
        ('Switzerland', 'Geneva - Permanent Mission'),
        ('United Kingdom', 'London'),
    ],
    'Middle_East': [
        ('Iran', 'Tehran'),
        ('Israel', 'Tel Aviv'),
        ('Kuwait', 'Kuwait City'),
        ('Oman', 'Muscat'),
        ('Qatar', 'Doha'),
        ('Saudi Arabia', 'Riyadh & Jeddah Consulate'),
        ('United Arab Emirates', 'Abu Dhabi & Dubai Consulate'),
    ],
    'Americas': [
        ('Brazil', 'Brasília'),
        ('Canada', 'Ottawa'),
        ('Cuba', 'Havana'),
        ('United States', 'Washington D.C.'),
        ('United States', 'New York - Permanent Mission'),
        ('United States', 'Los Angeles Consulate'),
    ],
    'Multilateral': [
        ('Kenya', 'United Nations Office at Nairobi (UNON)'),
        ('United States', 'United Nations, New York'),
        ('France', 'UNESCO, Paris'),
    ]
}

# A simple mapping to provide valid timezones based on city/country name
def get_timezone(city, country, region):
    mapping = {
        'Algiers': 'Africa/Algiers', 'Luanda': 'Africa/Luanda', 'Gaborone': 'Africa/Gaborone',
        'Bujumbura': 'Africa/Bujumbura', 'Kinshasa': 'Africa/Kinshasa', 'Djibouti': 'Africa/Djibouti',
        'Cairo': 'Africa/Cairo', 'Addis Ababa': 'Africa/Addis_Ababa', 'Accra': 'Africa/Accra',
        'Abidjan': 'Africa/Abidjan', 'Rabat': 'Africa/Casablanca', 'Maputo': 'Africa/Maputo',
        'Windhoek': 'Africa/Windhoek', 'Abuja': 'Africa/Lagos', 'Kigali': 'Africa/Kigali',
        'Dakar': 'Africa/Dakar', 'Mogadishu': 'Africa/Mogadishu', 'Pretoria': 'Africa/Johannesburg',
        'Juba': 'Africa/Juba', 'Khartoum': 'Africa/Khartoum', 'Dar es Salaam': 'Africa/Dar_es_Salaam',
        'Kampala': 'Africa/Kampala', 'Lusaka': 'Africa/Lusaka', 'Harare': 'Africa/Harare',
        'Canberra': 'Australia/Canberra', 'Beijing': 'Asia/Shanghai', 'New Delhi': 'Asia/Kolkata',
        'Jakarta': 'Asia/Jakarta', 'Tokyo': 'Asia/Tokyo', 'Kuala Lumpur': 'Asia/Kuala_Lumpur',
        'Islamabad': 'Asia/Karachi', 'Seoul': 'Asia/Seoul', 'Bangkok': 'Asia/Bangkok',
        'Vienna': 'Europe/Vienna', 'Brussels': 'Europe/Brussels', 'Paris': 'Europe/Paris',
        'Berlin': 'Europe/Berlin', 'Dublin': 'Europe/Dublin', 'Rome': 'Europe/Rome',
        'The Hague': 'Europe/Amsterdam', 'Moscow': 'Europe/Moscow', 'Madrid': 'Europe/Madrid',
        'Stockholm': 'Europe/Stockholm', 'Geneva': 'Europe/Zurich', 'London': 'Europe/London',
        'Tehran': 'Asia/Tehran', 'Tel Aviv': 'Asia/Jerusalem', 'Kuwait City': 'Asia/Kuwait',
        'Muscat': 'Asia/Muscat', 'Doha': 'Asia/Qatar', 'Riyadh': 'Asia/Riyadh',
        'Abu Dhabi': 'Asia/Dubai', 'Brasília': 'America/Sao_Paulo', 'Ottawa': 'America/Toronto',
        'Havana': 'America/Havana', 'Washington': 'America/New_York', 'New York': 'America/New_York',
        'Los Angeles': 'America/Los_Angeles', 'Nairobi': 'Africa/Nairobi'
    }
    for key, tz in mapping.items():
        if key in city or key in country:
            return tz
            
    if region == 'Africa': return 'Africa/Nairobi'
    if region == 'Europe': return 'Europe/London'
    if region == 'Asia': return 'Asia/Dubai'
    if region == 'Middle_East': return 'Asia/Riyadh'
    if region == 'Americas': return 'America/New_York'
    return 'UTC'

count = 0
for region, locations in missions_data.items():
    for country, city in locations:
        name = f"Mission {city}" if region != 'Multilateral' else city
        tz = get_timezone(city, country, region)
        
        # Working week logic (Gulf states Sun-Thu)
        working_week_start = 1 # Monday
        working_week_end = 5 # Friday
        if region == 'Middle_East' and country not in ['Israel', 'Iran']:
            working_week_start = 7 # Sunday
            working_week_end = 4 # Thursday

        mission, created = Mission.objects.get_or_create(
            name=name,
            defaults={
                'country': country,
                'city': city,
                'region': region,
                'timezone': tz,
                'working_week_start': working_week_start,
                'working_week_end': working_week_end,
                'work_start_time': '09:00',
                'work_end_time': '17:00',
                'status': 'Active'
            }
        )
        if created:
            count += 1
            print(f"Created: {name} in {country}")
        else:
            # Update region if needed
            mission.region = region
            mission.save()

print(f"\\nSuccessfully inserted {count} new missions. Total missions in DB: {Mission.objects.count()}")
