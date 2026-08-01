from django.core.management.base import BaseCommand
from django.db import transaction
from departments.models import Department
from accounts.models import User
from complaints.models import Complaint
from tests.factories import CitizenFactory, DepartmentFactory, OfficerFactory, ComplaintFactory
from django.db.models import Q
import random
import sys

class Command(BaseCommand):
    help = 'Seeds the database with dummy data for demonstration'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=30, help='Number of complaints to generate')
        parser.add_argument('--clear', action='store_true', help='Clear existing complaints before seeding')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        count = kwargs['count']
        
        self.stdout.write('Starting database seed process...')
        
        # 1. Create or ensure core specific departments exist
        self.stdout.write('Checking core departments...')
        dept_names = ['Electricity & Power', 'Water & Sewage', 'Road & Safety', 'Sanitation & Waste']
        departments = []
        for name in dept_names:
            dept, created = Department.objects.get_or_create(name=name)
            departments.append(dept)
            if created:
                self.stdout.write(f'Created missing core department: {name}')
        
        # 2. Create predictable citizens
        if not User.objects.filter(username='citizen1').exists():
            self.stdout.write('Creating predictable citizens...')
            User.objects.create_user(username='citizen1', email='citizen1@example.com', password='testpass123', role='citizen', first_name='Ramesh', last_name='Kumar')
            User.objects.create_user(username='citizen2', email='citizen2@example.com', password='testpass123', role='citizen', first_name='Suresh', last_name='Rao')
        
        citizens = list(User.objects.filter(role='citizen'))
            
        # 3. Create deterministic officers across all hierarchy levels for core departments
        self.stdout.write('Ensuring hierarchy officers for core departments...')
        officers = []
        for dept in departments:
            prefix = dept.name.split()[0].lower() # e.g., 'electricity', 'water', 'road', 'sanitation'
            roles = [
                ('staff', f'{prefix}_staff'),
                ('hod', f'{prefix}_hod'),
                ('district_officer', f'{prefix}_do')
            ]
            
            for role, username in roles:
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': f'{username}@example.com',
                        'role': role,
                        'department': dept,
                        'first_name': dept.name.split()[0],
                        'last_name': role.upper()
                    }
                )
                if created:
                    user.set_password('testpass123')
                    user.save()
                    self.stdout.write(f'Created {role} officer: {username}')
                officers.append(user)
                
        # 3.5 Create an admin superuser for testing and dashboard access
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin',
                role='state_admin'
            )
            self.stdout.write(self.style.SUCCESS('Created superuser account: username="admin", password="admin"'))
            
        # 3.8 Identify and wipe legacy out-of-bounds data
        out_of_bounds = Complaint.objects.filter(
            Q(latitude__lt=8.0) | Q(latitude__gt=37.0) | 
            Q(longitude__lt=68.0) | Q(longitude__gt=97.0)
        )
        if out_of_bounds.exists() or kwargs.get('clear'):
            self.stdout.write(self.style.WARNING("Found legacy complaints outside India (or --clear passed). Wiping all complaints to re-seed..."))
            Complaint.objects.all().delete()
            
        # 4. Create complaints only if none exist
        if Complaint.objects.count() == 0:
            self.stdout.write(f'Creating {count} complaints...')
            for _ in range(count):
                citizen = random.choice(citizens)
                department = random.choice(departments)
                status = random.choice(['pending', 'in_progress', 'resolved', 'escalated'])
                urgency = random.choice(['low', 'medium', 'high', 'critical'])
                
                ComplaintFactory(
                    created_by=citizen,
                    department=department,
                    status=status,
                    urgency_level=urgency
                )
            self.stdout.write(self.style.SUCCESS(f'Created {count} initial complaints.'))
        else:
            self.stdout.write(self.style.WARNING(f'Database already contains {Complaint.objects.count()} complaints. Skipping fake complaint generation.'))
            
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded the database!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} departments, {len(citizens)} citizens, {len(officers)} officers, and {count} complaints.'))
