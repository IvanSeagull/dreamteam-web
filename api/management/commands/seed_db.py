import random
import string
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import CustomUser, Hobby

# Sample hobby data
HOBBY_DATA = [
    ("football", "Playing football outdoors"),
    ("basketball", "Playing basketball in a court"),
    ("gaming", "Playing video games"),
    ("painting", "Painting on canvas or digitally"),
    ("guitar", "Playing guitar, acoustic or electric"),
    ("cooking", "Cooking or baking in the kitchen"),
    ("reading", "Reading books, articles, magazines"),
    ("writing", "Creative writing, journaling"),
    ("running", "Jogging or running marathons"),
    ("chess", "Playing chess competitively or for fun"),
]

FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Edward", 
               "Fiona", "George", "Hannah", "Ian", "Jane"]
LAST_NAMES  = ["Smith", "Jones", "Brown", "Taylor", "Williams", 
               "Miller", "Davis", "Garcia", "Wilson", "Thompson"]

NUM_USERS = 20

class Command(BaseCommand):
    help = "Seeds the database with sample hobbies and test users (no admin)."

    def handle(self, *args, **options):
        self.stdout.write("Starting the seeding process...")

        # 1. Create Hobbies
        self.create_hobbies()

        # 2. Create Test Users
        self.create_test_users()

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))

    def create_hobbies(self):
        """Create or get existing hobbies from HOBBY_DATA."""
        for name, desc in HOBBY_DATA:
            hobby, created = Hobby.objects.get_or_create(
                name=name,
                defaults={"description": desc}
            )
            if created:
                self.stdout.write(f"Created hobby: {hobby.name}")
            else:
                self.stdout.write(f"Hobby already exists: {hobby.name}")

    def create_test_users(self):
        """Create 20 test users with random data."""
        for i in range(NUM_USERS):
            # Generate a random full name
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            user_full_name = f"{first_name} {last_name}"

            # Create a random username
            username = self.generate_username(first_name, last_name, i)

            # Create an email
            email = f"{username}@example.com".lower()

            # Generate a random date of birth between ~15 to ~40 years old
            random_days = random.randint(15*365, 40*365)  
            date_of_birth = timezone.now().date() - timedelta(days=random_days)

            # If user with same username already exists, skip creation
            if CustomUser.objects.filter(username=username).exists():
                self.stdout.write(f"User {username} already exists; skipping.")
                continue

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password="testpassword",  # default password for easy login
                name=user_full_name,
                date_of_birth=date_of_birth
            )
            
            # Assign random subset of hobbies (0-5 of them)
            all_hobby_ids = list(Hobby.objects.values_list('id', flat=True))
            random.shuffle(all_hobby_ids)
            subset_size = random.randint(0, 5)
            chosen_hobbies = all_hobby_ids[:subset_size]
            user.hobbies.set(chosen_hobbies)
            
            self.stdout.write(f"Created user: {user.username} with {subset_size} hobbies.")

    def generate_username(self, first: str, last: str, index: int) -> str:
        """Generate a unique username like 'alice-smith-1'."""
        # Could add random letters or digits as well
        base = f"{first.lower()}-{last.lower()}-{index}"
        # Remove spaces or invalid chars
        return "".join(ch if ch.isalnum() or ch == '-' else "" for ch in base)
