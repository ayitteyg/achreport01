from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os



class Command(BaseCommand):
    help = 'Create a superuser with custom fields'

    def add_arguments(self, parser):
        parser.add_argument('--contact', default='0549053295', help='User contact number')
        parser.add_argument('--password', default='my-mtn-0549', help='User password')
        parser.add_argument('--department', default='admin', help='Department')
        parser.add_argument('--name', default='developer', help='Full name')
        parser.add_argument('--church', default='Achimota', help='Church')

    def handle(self, *args, **options):
        User = get_user_model()
        
        try:
            # Create superuser with only required fields first
            user = User.objects.create_superuser_custom(
                contact=options['contact'],
                password=options['password'],
                department=options['department']
            )
            
            # Update additional fields
            user.name = options['name']
            user.church = options['church']
            user.save()
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created superuser: {user.contact}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))