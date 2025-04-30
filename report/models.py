from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
""" 

CLEANING MODELS/RESETTING DATABASE
.clean/delete all migration files excepts init.py
.rm -rf db.sqlite3 #this delete the database
.python manage.py makemigrations 
.python manage.py migrate
.python manage.py createsupersuer

"""


RATING_CHOICES = [
        ('Poor', 'Poor'),
        ('Fair', 'Fair'),
        ('Good', 'Good'),
        ('Very Good', 'Very Good'),
        ('Excellent', 'Excellent'),
    ]

CHURCH = [("Achimota", "Achimota"), ("Prince of Peace", "Prince of Peace"), ("King of Glory", "King of Glory"),
                 ("Nii Boi Town", "Nii Boi Town"),("Israel", "Israel")]

typ = [("local", "local"), ("district", "district"), ("zonal", "zonal"), ("conference", "conference")]

MALE = 'M'
FEMALE = 'F'
GENDER_CHOICES = [(MALE, 'Male'), (FEMALE, 'Female')]

TRANSFER_TYPE_CHOICES = [
    ('transfer_in', 'Transfer In'),
    ('transfer_out', 'Transfer Out')
]

TRANSFER_STATUS = [
    ('complete', 'Complete'),
    ('pending', 'Pending')
]



DEPARTMENT_CHOICES = (
    ('Treasury', 'Treasury'),
    ('Secretariat', 'Secretariat'),
    ('Deaconry', 'Deaconry'),
    ('Sabbath School', 'Sabbath School'),
    ('Religious Liberty/VOP', 'Religious Liberty/VOP'),
    ('Health', 'Health'),
    ('Stewardship', 'Stewardship'),
    ('Personal Ministry', 'Personal Ministry'),
    ('Possibility Ministry', 'Possibility Ministry'),
    ('Communication', 'Communication'),
    ('Children Ministry', 'Children Ministry'),
    ('Publishing Ministry', 'Publishing Ministry'),
    ('Music', 'Music'),
    ('Adventist Men Ministry', 'Adventist Men Ministry'),
    ('Womens Ministry', 'Womens Ministry'),
    ('Audit', 'Audit'),
    ('Youth', 'Youth'),
    ('Family Ministry', 'Family Ministry'),
    ('Education', 'Education'),
    ('Welfare', 'Welfare'),
    ('PA System', 'PA System'),
    ('Interest Coordinator', 'Interest Coordinator'),
    ('Community Service', 'Community Service'),
    ('Project', 'Project'),
    ('Congregation', 'Congregation'),
    ('admin', 'admin'),
)



class Pastor(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Store pastor's name names dynamically
    def __str__(self):
        return self.name
    


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Store department names dynamically
    def __str__(self):
        return self.name


# class AppUser(AbstractUser):
#     name = models.CharField(max_length=50, blank=True)
#     church = models.CharField(max_length=25, choices=CHURCH)
#     department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
#     contact = models.CharField(max_length=10, blank=True)
    
#     # Role flags
#     is_local = models.BooleanField(default=False)
#     is_district = models.BooleanField(default=False)
#     is_officer = models.BooleanField(default=False)
    
#     # Add any additional fields here
    
#     def __str__(self):
#         return self.name



# class AppUserManager(BaseUserManager):
#     use_in_migrations = True

#     def _create_user(self, contact, password, **extra_fields):
#         if not contact:
#             raise ValueError('The Contact field must be set')
#         user = self.model(contact=contact, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, contact, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(contact, password, **extra_fields)

#     def create_superuser(self, contact, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self._create_user(contact, password, **extra_fields)


class AppUserManager(BaseUserManager):
    use_in_migrations = True  # Add this for proper migration support

    def _create_user(self, contact, password, **extra_fields):
        """
        Creates and saves a User with the given contact and password.
        """
        if not contact:
            raise ValueError('The Contact field must be set')
        
        # Normalize contact if needed (e.g., remove spaces, special characters)
        contact = self.normalize_contact(contact)
        
        user = self.model(contact=contact, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, contact, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(contact, password, **extra_fields)

    def create_superuser(self, contact, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(contact, password, **extra_fields)

    def normalize_contact(self, contact):
        """
        Normalize the contact by removing any unwanted characters.
        """
        # Example: Remove all non-digit characters
        import re
        return re.sub(r'[^\d]', '', contact)



# class AppUser(AbstractUser):
#     name = models.CharField(max_length=50, blank=True)
#     church = models.CharField(max_length=25, choices=CHURCH)
#     department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
#     contact = models.CharField(max_length=10, blank=True, unique=True)  # Make contact unique
    
#     # Role flags
#     is_local = models.BooleanField(default=False)
#     is_district = models.BooleanField(default=False)
#     is_officer = models.BooleanField(default=False)
    
#     USERNAME_FIELD = 'contact'  # Use contact as the username
#     REQUIRED_FIELDS = ['department']  # Required when creating superuser
    
#     objects = AppUserManager()  # Add this line
    
#     def save(self, *args, **kwargs):
#         if not self.pk:  # Only for new users
#             self.set_password(f"{self.contact}{self.department}")
#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return self.name
    
    
class AppUser(AbstractUser):
    # Remove username from fields
    username = None
    
    # Your existing fields
    name = models.CharField(max_length=50, blank=True)
    church = models.CharField(max_length=25, choices=CHURCH)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    contact = models.CharField(max_length=10, unique=True)  # Make sure this is unique
    
    # Role flags
    is_local = models.BooleanField(default=False)
    is_district = models.BooleanField(default=False)
    is_officer = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = ['department']  # Fields required when creating superuser
    
    # Remove the auto-password generation if you want manual control
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name






class Activity(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link activity to a user
    church =  models.CharField( default="Achimota",
        max_length=20,
        choices=CHURCH
    )
    department = models.CharField( max_length=50, choices=DEPARTMENT_CHOICES, default="")
    
    program = models.CharField(max_length=255)
    date = models.DateField()
    typ = models.CharField(default="conference",
        max_length=10,
        choices=typ
    )
    facilitator = models.CharField(max_length=255, blank=True, null=True)
    expense = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    rating = models.CharField(
        default='Good',
        choices=RATING_CHOICES,  # Updated to use the new rating options
        blank=True,
        null=True,
        max_length=20,
    )

   

    def __str__(self):
        return f"{self.program} ({self.date})"
    
    
    
    
class Baptism(models.Model):
    typ = models.CharField(max_length=10, choices=typ, default="local")
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_church_voted = models.DateField()
    date_baptized = models.DateField()
    church= models.CharField(max_length=25, choices=CHURCH)
    minutes_number = models.CharField(max_length=100)
    baptized_by = models.CharField(max_length=255)
    place_baptized = models.CharField(max_length=255)
    mothers_name = models.CharField(max_length=255, blank=True, null=True)
    fathers_name = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.other_names or ''} - {self.date_baptized}"



class Transfer(models.Model):
    # Model fields corresponding to the SQL schema
    church = models.CharField(max_length=25, choices=CHURCH, default="Achimota")
    typ = models.CharField(max_length=15, choices=TRANSFER_TYPE_CHOICES, default='transfer_in')
    first_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_church_voted = models.DateField()
    minutes_number = models.CharField(max_length=100)
    sending_church = models.CharField(max_length=255, blank=True, null=True)
    receiving_church = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=TRANSFER_STATUS, default='pending')
    contact = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.other_names or ''} - {self.typ} ({self.status})"
    
    

class Attendance(models.Model):
    SERVICE_CHOICES = [
        ("Mid-Week Service", "Mid-Week Service"),
        ("Bible Studies", "Bible Studies"),
        ("Sabbath School", "Sabbath School"),
        ("Divine Service", "Divine Service"),
        ("Others", "Others"),
    ]

    church = models.CharField(max_length=25, choices=CHURCH, default="")
    date = models.DateField()
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    adult = models.PositiveIntegerField()
    youth = models.PositiveIntegerField()
    children = models.PositiveIntegerField()
  

    def __str__(self):
        return f"{self.church} - {self.service} on {self.date}"
    
    
    
class Visitor(models.Model):
    STATUS_CHOICES = [
        ("adventist", "Adventist"),
        ("non_adventist", "Non-Adventist"),
    ]

    church = models.CharField(max_length=25, choices=CHURCH, default="Achimota")
    date = models.DateField()
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255, default="")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
    
    

class Dedication(models.Model):
    church = models.CharField(max_length=25, choices=CHURCH)
    date = models.DateField()
    child_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.child_name} - {self.date}"
    
    

class Event(models.Model):
    EVENT_TYPES = [
        ("Marriage", "Marriage"),
        ("Funeral", "Funeral"),
        ("Communion", "Communion"),
        ("Community service", "Community service"),
        ("Outreach/Visitation", "Outreach/Visitation"),
        ("Child birth", "Child birth"),
        ("Other", "Other"),
    ]

    church = models.CharField(max_length=25, choices=CHURCH, default="Achimota")
    date = models.DateField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_place = models.CharField(max_length=255)
    member_involved = models.CharField(max_length=255)
    event_detail = models.TextField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.event_type} - {self.date}"