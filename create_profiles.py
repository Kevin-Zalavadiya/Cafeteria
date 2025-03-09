import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parlour.settings')
django.setup()

from django.contrib.auth.models import User
from rai.models import Profile

# Create profiles for all users that don't have one
users_without_profiles = []
for user in User.objects.all():
    try:
        # Try to access the profile to check if it exists
        profile = user.profile
        print(f"User '{user.username}' already has a profile.")
    except:
        # If accessing the profile fails, create one
        profile = Profile.objects.create(user=user)
        profile.save()
        users_without_profiles.append(user.username)
        print(f"Created profile for user '{user.username}'")

if users_without_profiles:
    print(f"\nCreated profiles for {len(users_without_profiles)} users: {', '.join(users_without_profiles)}")
else:
    print("\nAll users already have profiles.")
