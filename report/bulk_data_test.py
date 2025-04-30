from .models import Baptism, Transfer, Attendance, Visitor, Event, Dedication, Department, Activity
from faker import Faker
from random import choice
from random import choice, randint, uniform
from django.contrib.auth import get_user_model




fake = Faker()


RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]

CHURCH = [("Achimota", "Achimota"), ("Prince of Peace", "Prince of Peace"), ("King of Glory", "King of Glory"),
                 ("Nii Boi Town", "Nii Boi Town"),("Israel", "Israel")]

TYP_CHOICES = [("local", "Local"), ("district", "District"), ("conference", "Conference")]

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


SERVICE_TYPES = [
    ('sunday', 'Sunday Service'),
    ('bible_study', 'Bible Study'),
    ('prayer_meeting', 'Prayer Meeting'),
    ('special', 'Special Service')
]


STATUS_CHOICES = [
        ("adventist", "Adventist"),
        ("non_adventist", "Non-Adventist"),
    ]



EVENT_TYPES = [
        ("Marriage", "Marriage"),
        ("Funeral", "Funeral"),
        ("Communion", "Communion"),
        ("Community service", "Community service"),
        ("Outreach/Visitation", "Outreach/Visitation"),
        ("Child birth", "Child birth"),
        ("Other", "Other"),
    ]




DEPARTMENT_CHOICES = (
    ('Treasury', 'Treasury'),
    ('Secretariat', 'Secretariat'),
    ('Head_Deacon', 'Head Deacon'),
    ('Head_Deaconess', 'Head Deaconess'),
    ('Sabbath_School', 'Sabbath School'),
    ('Religious_Liberty_VOP', 'Religious Liberty/VOP'),
    ('Health', 'Health'),
    ('Stewardship', 'Stewardship'),
    ('Personal_Ministry', 'Personal Ministry'),
    ('Possibility_Ministry', 'Possibility Ministry'),
    ('Communication', 'Communication'),
    ('Children_Ministry', 'Children Ministry'),
    ('Publishing_Ministry', 'Publishing Ministry'),
    ('Music_Director', 'Music Director'),
    ('Adventist_Men_Ministry', 'Adventist Men Ministry'),
    ('Womens_Ministry', 'Womens Ministry'),
    ('Audit', 'Audit'),
    ('Adventurer', 'Adveturer'),
    ('Young_Adult', 'Young Adult'),
    ('Public_Campus_Ministry', 'Public Campus Ministry'),
    ('Ambassador', 'Ambassador'),
    ('Pathfinder', 'Pathfinder'),
    ('Family_Ministry', 'Family Ministry'),
    ('Education', 'Education'),
    ('Welfare', 'Welfare'),
    ('Personal_Ministry_Sec', 'Personal Ministry Sec'),
    ('Pa_System', 'PA System'),
    ('Interest_Coordinator', 'Interest Coordinator'),
    ('Community_Service', 'Community Service'),
    ('Project', 'Project'),
)




# Generate 500 random Baptism records
def load_bulk_baptism():   
    baptism_objects = []
    for _ in range(50):
        baptism_objects.append(Baptism(
            typ=choice([typ[0] for typ in TYP_CHOICES]),  # Randomly pick from typ choices
            date_of_birth=fake.date_of_birth(minimum_age=1, maximum_age=100),  # Random date of birth
            first_name=fake.first_name(),
            other_names=fake.last_name(),
            gender=choice([gender[0] for gender in GENDER_CHOICES]),  # Randomly pick Male or Female
            date_church_voted=fake.date_between(start_date="-10y", end_date="-1y"),  # Random vote date in the past
            date_baptized=fake.date_between(start_date="-5y", end_date="today"),  # Random baptism date
            church=choice([church[0] for church in CHURCH]),  # Randomly pick a church
            minutes_number=fake.bothify(text='???-####'),  # Random minutes number (e.g., ABC-1234)
            baptized_by=fake.name(),  # Random name for who baptized
            place_baptized=fake.city(),  # Random city for baptism place
            mothers_name=fake.first_name() if choice([True, False]) else None,  # Random mother name or None
            fathers_name=fake.first_name() if choice([True, False]) else None,  # Random father name or None
            contact=fake.phone_number() if choice([True, False]) else None  # Random contact number or None
        ))

    # Bulk create the baptism records
    Baptism.objects.bulk_create(baptism_objects)

    print(f"{len(baptism_objects)} baptism records created.")



def load_bulk_transfer():
    transfer_objects = []
    for _ in range(50):  # Generate 50 records (adjust as needed)
        transfer_type = choice([typ[0] for typ in TRANSFER_TYPE_CHOICES])
        
        # Set sending/receiving churches based on transfer type
        if transfer_type == 'transfer_in':
            sending_church = choice([church[0] for church in CHURCH])
            receiving_church = "Achimota"  # Default receiving church
        elif transfer_type == 'transfer_out':
            sending_church = "Achimota"  # Default sending church
            receiving_church = choice([church[0] for church in CHURCH])
        else:  # Letter
            sending_church = choice([church[0] for church in CHURCH])
            receiving_church = choice([c[0] for c in CHURCH if c[0] != sending_church])
        
        transfer_objects.append(Transfer(
            church= choice([church[0] for church in CHURCH]), #,  # Default church
            typ=transfer_type,
            first_name=fake.first_name(),
            other_names=fake.last_name(),
            gender=choice([gender[0] for gender in GENDER_CHOICES]),
            date_church_voted=fake.date_between(start_date="-5y", end_date="today"),
            minutes_number=fake.bothify(text='TR-####-??'),  # e.g., TR-1234-AB
            sending_church=sending_church,
            receiving_church=receiving_church,
            status=choice([status[0] for status in TRANSFER_STATUS]),
            contact=fake.phone_number()[:10] if choice([True, False]) else None
        ))
    
    # Bulk create the transfer records
    Transfer.objects.bulk_create(transfer_objects)
    print(f"{len(transfer_objects)} transfer records created.")
    
    
    
def load_bulk_attendance(num_records=100):
    attendance_objects = []
    
    for _ in range(num_records):
        # Generate random date within last 2 years
        random_date = fake.date_between(start_date='-2y', end_date='today')
        
        # Generate random counts (adjust ranges as needed)
        random_count = randint(0, 50)
        attendance_objects.append(Attendance(
            date=random_date,
            service=choice([st[0] for st in SERVICE_TYPES]),
            church=choice([church[0] for church in CHURCH]),
            adult=random_count,
            youth=random_count,
            children=random_count,
        ))
    
    # Bulk create the attendance records
    Attendance.objects.bulk_create(attendance_objects)
    print(f"Successfully created {len(attendance_objects)} attendance records.")
    
    
    
    
def load_bulk_visitors(num_records=100):
    visitors = []
    status_choices = ["adventist", "non_adventist"]

    for _ in range(num_records):
        visitor = Visitor(
            church=choice([ch[0] for ch in CHURCH]),
            date=fake.date_between(start_date='-2y', end_date='today'),
            name=fake.name(),
            status=choice(status_choices),
            contact=fake.phone_number()
        )
        visitors.append(visitor)

    Visitor.objects.bulk_create(visitors)
    print(f"✅ Successfully created {len(visitors)} visitor records.")
    
    
    
def load_bulk_events(num_records=50):
    events = []

    for _ in range(num_records):
        event = Event(
            church=choice([ch[0] for ch in CHURCH]),
            date=fake.date_between(start_date='-2y', end_date='today'),
            event_type=choice([et[0] for et in EVENT_TYPES]),
            event_place=fake.city(),
            member_involved=fake.name(),
            event_detail=fake.sentence(nb_words=6),
            remarks=fake.text(max_nb_chars=30)
        )
        events.append(event)

    Event.objects.bulk_create(events)
    print(f"✅ Successfully created {len(events)} event records.")
    
    
    
def load_bulk_dedications(num_records=50):
    dedications = []

    for _ in range(num_records):
        dob = fake.date_of_birth(minimum_age=0, maximum_age=3)
        dedication = Dedication(
            church=choice([ch[0] for ch in CHURCH]),
            date=fake.date_between(start_date=dob, end_date='today'),
            child_name=fake.first_name() + " " + fake.last_name(),
            date_of_birth=dob,
            place_of_birth=fake.city(),
            mother_name=fake.name_female(),
            father_name=fake.name_male()
        )
        dedications.append(dedication)

    Dedication.objects.bulk_create(dedications)
    print(f"✅ Successfully created {len(dedications)} dedication records.")
    
    

def load_bulk_department():
    department_names = [
        "Treasury",
        "Secretariat",
        "Deaconry",
        "Sabbath School",
        "Religious Libert/Vop",
        "Health",
        "Stewardship",
        "Personal Ministry",
        "Possibility Ministry",
        "Communication",
        "Children Ministry",
        "Publishing Ministry",
        "Music",
        "Advetntist Men Ministry",
        "Womens Ministry",
        "Audit",
        "Youth",
        "Family Ministry",
        "Education",
        "Welfare",
        "PA System",
        "Interest Coordinator",
        "Community Service",
        "Project",
        "admin"
    ]

    created_count = 0
    for name in department_names:
        _, created = Department.objects.get_or_create(name=name)
        if created:
            created_count += 1

    print(f"{created_count} departments created.")
    



def load_bulk_activities(num_records=50):
    User = get_user_model()
    activities = []
    
    # Get all available users and departments
    users = User.objects.all()
    departments = Department.objects.all()
    
    for _ in range(num_records):
        activity = Activity(
            user=choice(users) if users.exists() else None,
            church=choice([ch[0] for ch in CHURCH]),
            department=choice(departments) if departments.exists() else None,
            program=fake.sentence(nb_words=5),
            date=fake.date_between(start_date='-2y', end_date='today'),
            typ=choice([typ[0] for typ in TYP_CHOICES]),
            facilitator=fake.name(),
            expense=round(uniform(0, 1000), 2),  # Random expense between 0-1000
            income=round(uniform(0, 2000), 2),  # Random income between 0-2000
            rating=choice([r[0] for r in RATING_CHOICES]),
            remarks=fake.text(max_nb_chars=100),
        )
        activities.append(activity)
    
    Activity.objects.bulk_create(activities)
    print(f"✅ Successfully created {len(activities)} activity records.")
    
    

def create_test_users():
    AppUser = get_user_model()
    fake = Faker()
    
   
    
    # Create users
    users = []
    
    # Superuser
    # admin = AppUser.objects.create_superuser(
    #     username='developer',
    #     email='ayittey.og@gamil.com',
    #     password='my-mtn-0549',
    #     name='Ayittey Odame George',
    #     church='Achimota',
    #     department='Secretariat',
    #     contact='0549053295',
    #     is_local=True,
    #     is_district=False,
    #     is_officer=False
    # )
    #users.append(admin)
    
    # Regular users
    # for i in range (1,4):
    #     user = AppUser.objects.create_user(
    #         username=f'user{i}',
    #         email=fake.email(),
    #         password=f'user{i}123',
    #         name=fake.name(),
    #         church=choice([ch[0] for ch in CHURCH]),
    #         department=choice([dpt[0] for dpt in DEPARTMENT_CHOICES]),
    #         contact=f'0244{fake.random_number(digits=6, fix_len=True)}',
    #         is_local=fake.boolean(chance_of_getting_true=70),
    #         is_district=fake.boolean(chance_of_getting_true=30),
    #         is_officer=fake.boolean(chance_of_getting_true=20)
    #     )
    #     users.append(user)
        
    
    user = AppUser.objects.create_user(
            username='Akwasi Owusu',
            email=fake.email(),
            password='owusu123',
            name=fake.name(),
            church='Achimota',
            department="Interest Coordinator",
            contact=f'0244{fake.random_number(digits=6, fix_len=True)}',
            is_local=True,
            is_district=False,
            is_officer=False
        )
    
    users.append(user)
        
    print(f"✅ Successfully created {len(users)} users data.")
    return users


#runing data
def run_data():
    # load_bulk_baptism()
    # load_bulk_transfer()
    # load_bulk_attendance()
    # load_bulk_visitors()
    # load_bulk_dedications()
    # load_bulk_activities()
    #load_bulk_department()
    # load_bulk_events()
    #create_test_users()
    pass