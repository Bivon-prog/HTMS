import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'htms.settings')
django.setup()

from apps.authentication.models import User

def backfill():
    users = User.objects.all()
    count = 0
    for user in users:
        if not user.user_id:
            user.save() # This will trigger the save method and generate the ID
            count += 1
            print(f"Assigned ID {user.user_id} to user {user.email}")

    print(f"Finished backfilling {count} users.")

if __name__ == '__main__':
    backfill()
