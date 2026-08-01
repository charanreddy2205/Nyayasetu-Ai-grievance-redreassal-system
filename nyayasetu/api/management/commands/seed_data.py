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
        
        # Check if we already have some data to prevent huge duplication
        if Department.objects.count() > 0:
            self.stdout.write(self.style.WARNING('Database already contains data! Skipping seed.'))
            return

        # 1. Create a few specific departments matching our AI fallback config
        self.stdout.write('Creating departments...')
        dept_names = ['Electricity & Power', 'Water & Sewage', 'Road & Safety', 'Sanitation & Waste']
        departments = []
        for name in dept_names:
            dept = DepartmentFactory(name=name)
            departments.append(dept)
        
        # 2. Create citizens
        self.stdout.write('Creating citizens...')
        citizens = CitizenFactory.create_batch(10)
        
        # 3. Create officers for the departments
        self.stdout.write('Creating officers...')
        officers = []
        for dept in departments:
            officer = OfficerFactory(department=dept)
            officers.append(officer)
            
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
