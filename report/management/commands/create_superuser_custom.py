from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create superuser with custom fields'

    def handle(self, *args, **options):
        User = get_user_model()
        
        try:
            user = User.objects.create_superuser(
                contact='0242534286',
                password='my-mtn-0549',
                department='admin',
                name='developer',
                church='Achimota'
            )
            self.stdout.write(self.style.SUCCESS(f'Created superuser: {user.contact}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))