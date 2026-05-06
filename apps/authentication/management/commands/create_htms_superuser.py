from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser for HTMS system'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True)
        parser.add_argument('--first_name', type=str, required=True)
        parser.add_argument('--last_name', type=str, required=True)
        parser.add_argument('--password', type=str, required=False)

    def handle(self, *args, **options):
        email = options['email']
        first_name = options['first_name']
        last_name = options['last_name']
        password = options.get('password', 'admin123')

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email {email} already exists.')
            )
            return

        try:
            user = User.objects.create_superuser(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser {email} created successfully!')
            )
            self.stdout.write(f'Login credentials: {email} / {password}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
