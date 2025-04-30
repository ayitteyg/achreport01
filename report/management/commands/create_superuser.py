from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os



class Command(BaseCommand):
    help = 'Create a superuser with custom fields'

    def handle(self, *args, **options):
        User = get_user_model()
        
        contact = '0549053295'  # or input('Contact: ')
        department = 'admin'     # or input('Department: ')
        name = 'developer'      # or input('Name: ')
        church = 'Achimota'            # or input('Church: ')
        
        try:
            user = User.objects.create_superuser(
                contact=contact,
                department=department,
                name=name,
                church=church,
                password='my-mtn-0549'  # Set a secure password
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {user}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))