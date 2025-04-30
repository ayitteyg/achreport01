from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create a superuser with custom fields'

    def handle(self, *args, **options):
        User = get_user_model()
        
        contact = '0549053295'
        department = 'admin'
        name = 'developer'
        church = 'Achimota'
        password = 'my-mtn-0549'
        
        try:
            user = User.objects.create_superuser(
                contact=contact,  # This matches USERNAME_FIELD
                password=password,  # Password must come right after USERNAME_FIELD
                # Additional required fields:
                department=department,
                # Optional fields:
                name=name,
                church=church,
                # Ensure superuser flags are set (they should be set automatically by your manager)
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {user}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))