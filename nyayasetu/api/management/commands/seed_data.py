from django.core.management.base import BaseCommand
from django.db import transaction
from departments.models import Department
from accounts.models import User
from complaints.models import Complaint
from tests.factories import CitizenFactory, DepartmentFactory, OfficerFactory, ComplaintFactory
import random
import sys

class Command(BaseCommand):
    help = 'Seeds the database with dummy data for demonstration'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=30, help='Number of complaints to generate')

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
        
        # 2. Create citizens if we have too few
        if User.objects.filter(role='citizen').count() < 5:
            self.stdout.write('Creating citizens...')
            citizens = CitizenFactory.create_batch(10)
        else:
            citizens = User.objects.filter(role='citizen')
            
        # 3. Create officers for the core departments if they lack them
        self.stdout.write('Ensuring officers for core departments...')
        officers = []
        for dept in departments:
            if not User.objects.filter(department=dept).exists():
                officer = OfficerFactory(department=dept)
                officers.append(officer)
                self.stdout.write(f'Created officer {officer.username} for {dept.name}')
            else:
                officers.append(User.objects.filter(department=dept).first())
            
        # 4. Create complaints
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
            
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded the database!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} departments, {len(citizens)} citizens, {len(officers)} officers, and {count} complaints.'))
