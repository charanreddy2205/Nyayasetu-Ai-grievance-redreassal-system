from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from departments.models import Department

User = get_user_model()


class Command(BaseCommand):
    help = 'Create deterministic demo users for local E2E testing.'

    def handle(self, *args, **options):
        department = Department.objects.first()
        if not department:
            self.stdout.write(self.style.WARNING('No departments found; skipping user seeding.'))
            return

        users = [
            {
                'username': 'test_citizen',
                'email': 'citizen@example.com',
                'password': 'testpass123',
                'role': 'citizen',
                'first_name': 'Test',
                'last_name': 'Citizen',
            },
            {
                'username': 'devansh12',
                'email': 'officer@example.com',
                'password': 'Charan@24',
                'role': 'staff',
                'first_name': 'Devansh',
                'last_name': 'Officer',
                'department': department,
            },
            {
                'username': 'ravi12',
                'email': 'ravi@example.com',
                'password': 'Charan@24',
                'role': 'citizen',
                'first_name': 'Ravi',
                'last_name': 'User',
            },
        ]

        for payload in users:
            username = payload['username']
            user = User.objects.filter(username=username).first()
            if not user:
                user = User.objects.create_user(
                    username=username,
                    email=payload['email'],
                    password=payload['password'],
                    first_name=payload.get('first_name', ''),
                    last_name=payload.get('last_name', ''),
                )
            user.role = payload['role']
            if payload.get('department'):
                user.department = payload['department']
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created/updated user {username}'))
