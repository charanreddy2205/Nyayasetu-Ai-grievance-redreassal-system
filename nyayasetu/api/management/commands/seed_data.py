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
        parser.add_argument('--count', type=int, default=50, help='Number of complaints to generate')
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
            
        # 3.8 Identify and wipe legacy out-of-bounds data or data lacking escalations
        from escalation.models import EscalationLog
        from complaints.models import ComplaintComment
        out_of_bounds = Complaint.objects.filter(
            Q(latitude__lt=8.0) | Q(latitude__gt=37.0) | 
            Q(longitude__lt=68.0) | Q(longitude__gt=97.0)
        )
        lacking_escalations = EscalationLog.objects.count() == 0
        
        us_states = [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
            "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
            "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
            "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
            "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", 
            "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", 
            "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
        ]
        has_us_states = Complaint.objects.filter(state__in=us_states).exists()
        
        # Check for rogue fake users that aren't our deterministic users
        allowed_usernames = ['citizen1', 'citizen2', 'admin']
        for d in departments:
            prefix = d.name.split()[0].lower()
            allowed_usernames.extend([f'{prefix}_staff', f'{prefix}_hod', f'{prefix}_do'])
            
        rogues_exist = User.objects.exclude(username__in=allowed_usernames).exists()
        
        if out_of_bounds.exists() or lacking_escalations or has_us_states or rogues_exist or kwargs.get('clear'):
            self.stdout.write(self.style.WARNING("Found legacy data, rogue users, or --clear passed. Wiping all complaints to re-seed timelines..."))
            
            # Use raw SQL to bypass Django's soft-delete ORM and bulk delete cascade traps
            from django.db import connection
            with connection.cursor() as cursor:
                if connection.vendor == 'postgresql':
                    cursor.execute("TRUNCATE TABLE complaints_complaintcomment CASCADE;")
                    cursor.execute("TRUNCATE TABLE escalation_escalationlog CASCADE;")
                    cursor.execute("TRUNCATE TABLE complaints_complaint CASCADE;")
                else:
                    cursor.execute("DELETE FROM complaints_complaintcomment;")
                    cursor.execute("DELETE FROM escalation_escalationlog;")
                    cursor.execute("DELETE FROM complaints_complaint;")
            
            # Now that all references are completely gone, we can safely purge rogue users
            User.objects.exclude(username__in=allowed_usernames).delete()
            self.stdout.write("Purged rogue fake users.")
            
        # 4. Create complaints only if none exist
        if Complaint.objects.count() == 0:
            from escalation.models import EscalationLog
            from complaints.models import ComplaintComment
            from django.utils import timezone
            from datetime import timedelta
            
            self.stdout.write(f'Creating {count} complaints with realistic timelines and escalations...')
            
            # Identify the state admin
            state_admin = User.objects.filter(role='state_admin').first()
            
            for i in range(count):
                citizen = random.choice(citizens)
                department = random.choice(departments)
                status = random.choice(['pending', 'in_progress', 'resolved'])
                urgency = random.choice(['low', 'medium', 'high', 'critical'])
                
                # Assign initially to staff using explicit deterministic usernames
                prefix = department.name.split()[0].lower()
                staff = User.objects.filter(username=f'{prefix}_staff').first()
                hod = User.objects.filter(username=f'{prefix}_hod').first()
                do = User.objects.filter(username=f'{prefix}_do').first()
                
                creation_time = timezone.now() - timedelta(days=random.randint(1, 15))
                
                complaint = ComplaintFactory(
                    created_by=citizen,
                    department=department,
                    assigned_to=staff,
                    status=status,
                    urgency_level=urgency
                )
                
                # Backdate the creation time for timeline realism
                Complaint.objects.filter(id=complaint.id).update(created_at=creation_time)
                
                # Determine if this complaint should be escalated (about 40% chance)
                should_escalate = random.random() < 0.4
                
                if should_escalate and status != 'resolved':
                    complaint.status = 'escalated'
                    # Determine escalation depth (1=HOD, 2=DO, 3=State Admin)
                    depth = random.choice([1, 2, 3])
                    current_time = creation_time + timedelta(days=1)
                    
                    if depth >= 1 and hod:
                        EscalationLog.objects.create(
                            complaint=complaint, escalated_to=hod,
                            reason="SLA Breached at Staff level."
                        )
                        EscalationLog.objects.filter(id=EscalationLog.objects.last().id).update(escalated_at=current_time)
                        complaint.assigned_to = hod
                        complaint.escalation_level = 1
                        
                    if depth >= 2 and do:
                        current_time += timedelta(days=2)
                        EscalationLog.objects.create(
                            complaint=complaint, escalated_to=do,
                            reason="SLA Breached at HOD level."
                        )
                        EscalationLog.objects.filter(id=EscalationLog.objects.last().id).update(escalated_at=current_time)
                        complaint.assigned_to = do
                        complaint.escalation_level = 2
                        
                    if depth == 3 and state_admin:
                        current_time += timedelta(days=3)
                        EscalationLog.objects.create(
                            complaint=complaint, escalated_to=state_admin,
                            reason="SLA Breached at District Officer level."
                        )
                        EscalationLog.objects.filter(id=EscalationLog.objects.last().id).update(escalated_at=current_time)
                        complaint.assigned_to = state_admin
                        complaint.escalation_level = 3
                        
                    complaint.save()
                    
            self.stdout.write(self.style.SUCCESS(f'Created {count} initial complaints.'))
        else:
            self.stdout.write(self.style.WARNING(f'Database already contains {Complaint.objects.count()} complaints. Skipping fake complaint generation.'))
            
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded the database!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} departments, {len(citizens)} citizens, {len(officers)} officers, and {count} complaints.'))
        
        # Clear dashboard cache so new states show up immediately
        from django.core.cache import cache
        cache.clear()
        self.stdout.write(self.style.SUCCESS('Cleared application cache.'))
