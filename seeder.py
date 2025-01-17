# seeder.py
import os
import sys
import django
from datetime import date, timedelta
import random

# Add the project root directory to the Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)  # Changed this line

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')  # Changed this line
try:
    django.setup()
except Exception as e:
    print(f"Failed to setup Django: {e}")
    sys.exit(1)

# Import models after Django setup
try:
    from api.models import Hobby, CustomUser
except Exception as e:
    print(f"Failed to import models: {e}")
    sys.exit(1)

def create_hobbies():
    """Create predefined hobbies"""
    hobbies_data = [
        {"name": "Reading", "description": "Enjoying books and literature"},
        {"name": "Gaming", "description": "Playing video games"},
        {"name": "Cooking", "description": "Preparing and experimenting with food"},
        {"name": "Photography", "description": "Taking and editing photos"},
        {"name": "Hiking", "description": "Outdoor walking and exploration"},
        {"name": "Painting", "description": "Creating art with paint"},
        {"name": "Music", "description": "Playing instruments or listening to music"},
        {"name": "Programming", "description": "Writing code and developing software"},
        {"name": "Gardening", "description": "Growing and maintaining plants"},
        {"name": "Dancing", "description": "Moving to rhythm and music"},
        {"name": "Writing", "description": "Creating written content"},
        {"name": "Chess", "description": "Playing strategic board games"},
        {"name": "Yoga", "description": "Physical and mental exercise"},
        {"name": "Swimming", "description": "Water-based exercise"},
        {"name": "Cycling", "description": "Riding bicycles for leisure or sport"}
    ]

    created_hobbies = []
    for hobby_data in hobbies_data:
        hobby, created = Hobby.objects.get_or_create(
            name=hobby_data["name"],
            defaults={"description": hobby_data["description"]}
        )
        created_hobbies.append(hobby)
        if created:
            print(f"Created hobby: {hobby.name}")
    return created_hobbies

def generate_random_date(start_year=1970, end_year=2005):
    """Generate a random birth date"""
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)

def create_users(hobbies, num_users=20):
    """Create test users with random hobbies"""
    # Create admin user if it doesn't exist
    admin_user, created = CustomUser.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'name': 'Admin User',
            'date_of_birth': date(1990, 1, 1),
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Created admin user")
        # Add random hobbies to admin
        admin_hobbies = random.sample(hobbies, random.randint(3, 6))
        admin_user.hobbies.set(admin_hobbies)

    # Create regular test users
    for i in range(num_users):
        username = f'user{i+1}'
        
        # Skip if user already exists
        if CustomUser.objects.filter(username=username).exists():
            continue

        user = CustomUser.objects.create(
            username=username,
            email=f'user{i+1}@example.com',
            name=f'Test User {i+1}',
            date_of_birth=generate_random_date()
        )
        user.set_password(f'password{i+1}')
        
        # Assign random hobbies (between 2 and 8 hobbies per user)
        user_hobbies = random.sample(hobbies, random.randint(2, 8))
        user.hobbies.set(user_hobbies)
        
        user.save()
        print(f"Created user: {username} with {len(user_hobbies)} hobbies")

def main():
    """Main seeder function"""
    print("Starting database seeding...")
    
    # Create hobbies
    print("\nCreating hobbies...")
    hobbies = create_hobbies()
    
    # Create users
    print("\nCreating users...")
    create_users(hobbies)
    
    print("\nSeeding completed!")
    
    # Print some statistics
    print("\nDatabase statistics:")
    print(f"Total hobbies: {Hobby.objects.count()}")
    print(f"Total users: {CustomUser.objects.count()}")
    
    # Print some test user credentials
    print("\nTest Credentials:")
    print("Admin user:")
    print("Username: admin")
    print("Password: admin123")
    print("\nTest users:")
    print("Username: user1, user2, ..., user20")
    print("Password: password1, password2, ..., password20")

if __name__ == "__main__":
    main()