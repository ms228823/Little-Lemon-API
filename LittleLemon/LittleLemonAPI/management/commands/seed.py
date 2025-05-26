"""
---------------------------------------------------------------------
Django Custom Management Command: seed_data
---------------------------------------------------------------------

This script populates the database with initial data, including:

- Default user groups: Manager, Delivery Crew
- Predefined users:
    - admin (superuser)
    - manager (assigned to "Manager" group)
    - delivery (assigned to "Delivery Crew" group)
    - customer (no group)
- Sample menu categories: Appetizers, Main Course
- Sample menu items:
    - Bruschetta (Appetizer)
    - Spaghetti Carbonara (Main Course)

Usage:
    python manage.py seed_data

This command is useful for setting up a development or testing environment quickly.
---------------------------------------------------------------------
"""


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from LittleLemonAPI.models import Category, MenuItem

class Command(BaseCommand):
    help = 'Seed database with initial data and users'

    def handle(self, *args, **kwargs):
        # Create groups
        groups = ['Manager', 'Delivery Crew']
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)
        
        # Create users
        users = {
            'admin': {'password': 'adminpass', 'is_staff': True, 'is_superuser': True},
            'manager': {'password': 'managerpass', 'group': 'Manager'},
            'delivery': {'password': 'deliverypass', 'group': 'Delivery Crew'},
            'customer': {'password': 'customerpass'},
        }

        for username, info in users.items():
            user, created = User.objects.get_or_create(username=username)
            user.set_password(info['password'])
            user.is_staff = info.get('is_staff', False)
            user.is_superuser = info.get('is_superuser', False)
            user.save()

            if 'group' in info:
                group = Group.objects.get(name=info['group'])
                user.groups.add(group)

        # Sample Categories
        appetizers = Category.objects.get_or_create(title="Appetizers", slug="appetizers")[0]
        mains = Category.objects.get_or_create(title="Main Course", slug="main-course")[0]

        # Sample Menu Items
        MenuItem.objects.get_or_create(title="Bruschetta", price=5.99, category=appetizers, featured=True)
        MenuItem.objects.get_or_create(title="Spaghetti Carbonara", price=12.99, category=mains, featured=False)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))
