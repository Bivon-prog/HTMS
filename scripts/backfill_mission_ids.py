import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'htms.settings')
django.setup()

from apps.missions.models import Mission

def backfill():
    missions = Mission.objects.all()
    count = 0
    for mission in missions:
        if not mission.mission_id:
            mission.save() # This will trigger the save method and generate the ID
            count += 1
            print(f"Assigned ID {mission.mission_id} to mission {mission.name}")

    print(f"Finished backfilling {count} missions.")

if __name__ == '__main__':
    backfill()
