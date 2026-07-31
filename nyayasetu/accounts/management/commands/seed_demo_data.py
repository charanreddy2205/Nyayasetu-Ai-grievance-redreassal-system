from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from complaints.models import Complaint, ComplaintComment
from departments.models import Department, DepartmentKeyword
from escalation.models import EscalationLog

User = get_user_model()


class Command(BaseCommand):
    help = 'Create rich demo data for departments, users, complaints, comments, and escalations.'

    def handle(self, *args, **options):
        departments_data = [
            {
                'name': 'State Administration',
                'description': 'Cross-department coordination and administrative oversight.',
                'sla_hours': 24,
                'transparency_score': 92.0,
                'keywords': ['administration', 'governance', 'policy', 'state'],
            },
            {
                'name': 'Health Department',
                'description': 'Public health, hospitals, sanitation, and medical emergencies.',
                'sla_hours': 36,
                'transparency_score': 88.5,
                'keywords': ['hospital', 'doctor', 'ambulance', 'health', 'clinic'],
            },
            {
                'name': 'Water Supply',
                'description': 'Water pipeline repairs and drinking water service issues.',
                'sla_hours': 48,
                'transparency_score': 81.0,
                'keywords': ['water', 'pipeline', 'tap', 'drinking', 'sewage'],
            },
            {
                'name': 'Transport Department',
                'description': 'Road maintenance, public transport, and traffic concerns.',
                'sla_hours': 40,
                'transparency_score': 85.2,
                'keywords': ['road', 'transport', 'traffic', 'bus', 'signal'],
            },
            {
                'name': 'Electricity Board',
                'description': 'Power outages, transformer faults, and meter issues.',
                'sla_hours': 30,
                'transparency_score': 79.4,
                'keywords': ['electricity', 'power', 'transformer', 'meter', 'wire'],
            },
            {
                'name': 'Education Department',
                'description': 'School infrastructure, admissions, and educational services.',
                'sla_hours': 60,
                'transparency_score': 90.3,
                'keywords': ['school', 'college', 'teacher', 'admission', 'education'],
            },
        ]

        departments = []
        for data in departments_data:
            department, created = Department.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'sla_hours': data['sla_hours'],
                    'transparency_score': data['transparency_score'],
                },
            )
            if not created:
                department.description = data['description']
                department.sla_hours = data['sla_hours']
                department.transparency_score = data['transparency_score']
                department.save()
            for word in data['keywords']:
                DepartmentKeyword.objects.get_or_create(department=department, word=word, defaults={'weight': 2})
            departments.append(department)

        users_payload = [
            {
                'username': 'state_admin_demo',
                'email': 'state.admin@example.com',
                'password': 'Password123!',
                'role': 'state_admin',
                'first_name': 'Ramesh',
                'last_name': 'Iyer',
                'department': departments[0],
            },
            {
                'username': 'district_officer_1',
                'email': 'district1@example.com',
                'password': 'Password123!',
                'role': 'district_officer',
                'first_name': 'Anita',
                'last_name': 'Rao',
                'department': departments[1],
            },
            {
                'username': 'district_officer_2',
                'email': 'district2@example.com',
                'password': 'Password123!',
                'role': 'district_officer',
                'first_name': 'Suresh',
                'last_name': 'Kumar',
                'department': departments[2],
            },
            {
                'username': 'hod_health',
                'email': 'hod.health@example.com',
                'password': 'Password123!',
                'role': 'hod',
                'first_name': 'Meera',
                'last_name': 'Sharma',
                'department': departments[1],
            },
            {
                'username': 'hod_transport',
                'email': 'hod.transport@example.com',
                'password': 'Password123!',
                'role': 'hod',
                'first_name': 'Karthik',
                'last_name': 'Menon',
                'department': departments[3],
            },
            {
                'username': 'staff_water',
                'email': 'staff.water@example.com',
                'password': 'Password123!',
                'role': 'staff',
                'first_name': 'Naveen',
                'last_name': 'Das',
                'department': departments[2],
            },
            {
                'username': 'staff_electricity',
                'email': 'staff.electricity@example.com',
                'password': 'Password123!',
                'role': 'staff',
                'first_name': 'Priya',
                'last_name': 'Joshi',
                'department': departments[4],
            },
            {
                'username': 'staff_education',
                'email': 'staff.education@example.com',
                'password': 'Password123!',
                'role': 'staff',
                'first_name': 'Varun',
                'last_name': 'Bhat',
                'department': departments[5],
            },
        ]

        created_users = {}
        for payload in users_payload:
            user, created = User.objects.get_or_create(
                username=payload['username'],
                defaults={
                    'email': payload['email'],
                    'first_name': payload['first_name'],
                    'last_name': payload['last_name'],
                    'role': payload['role'],
                    'department': payload['department'],
                    'is_active': True,
                },
            )
            if not created:
                user.email = payload['email']
                user.first_name = payload['first_name']
                user.last_name = payload['last_name']
                user.role = payload['role']
                user.department = payload['department']
                user.is_active = True
                user.save()
            user.set_password(payload['password'])
            user.save()
            created_users[payload['username']] = user

        citizens_payload = [
            {'username': 'citizen_one', 'email': 'citizen.one@example.com', 'first_name': 'Asha', 'last_name': 'Singh'},
            {'username': 'citizen_two', 'email': 'citizen.two@example.com', 'first_name': 'Bharat', 'last_name': 'Patel'},
            {'username': 'citizen_three', 'email': 'citizen.three@example.com', 'first_name': 'Chaitra', 'last_name': 'Nair'},
            {'username': 'citizen_four', 'email': 'citizen.four@example.com', 'first_name': 'Dinesh', 'last_name': 'Reddy'},
        ]
        for payload in citizens_payload:
            user, created = User.objects.get_or_create(
                username=payload['username'],
                defaults={
                    'email': payload['email'],
                    'first_name': payload['first_name'],
                    'last_name': payload['last_name'],
                    'role': 'citizen',
                    'is_active': True,
                },
            )
            if not created:
                user.email = payload['email']
                user.first_name = payload['first_name']
                user.last_name = payload['last_name']
                user.role = 'citizen'
                user.is_active = True
                user.save()
            user.set_password('Password123!')
            user.save()
            created_users[payload['username']] = user

        complaint_samples = [
            {
                'title': 'Water supply interruption near Ashok Vihar',
                'description': 'Residents have been without drinking water for the last two days, and the pipeline is leaking near the main junction.',
                'department': departments[2],
                'assigned_to': created_users['staff_water'],
                'created_by': created_users['citizen_one'],
                'status': 'pending',
                'urgency_level': 'high',
                'city': 'Hyderabad',
                'state': 'Telangana',
                'address': 'Ashok Vihar, Lane 4',
                'pincode': '500001',
                'latitude': Decimal('17.385044'),
                'longitude': Decimal('78.486671'),
                'contact_number': '9876543210',
                'created_at': timezone.now() - timedelta(days=1),
            },
            {
                'title': 'Streetlight outage on Main Road',
                'description': 'Several streetlights are not working near the school crossing, creating safety concerns during the evening commute.',
                'department': departments[4],
                'assigned_to': created_users['staff_electricity'],
                'created_by': created_users['citizen_two'],
                'status': 'in_progress',
                'urgency_level': 'medium',
                'city': 'Bengaluru',
                'state': 'Karnataka',
                'address': 'Main Road, Jayanagar',
                'pincode': '560011',
                'latitude': Decimal('12.971599'),
                'longitude': Decimal('77.594566'),
                'contact_number': '9123456780',
                'created_at': timezone.now() - timedelta(days=2),
            },
            {
                'title': 'Potholes on the school approach road',
                'description': 'Large potholes are harming traffic flow and risking school bus movement during morning hours.',
                'department': departments[3],
                'assigned_to': created_users['hod_transport'],
                'created_by': created_users['citizen_three'],
                'status': 'resolved',
                'urgency_level': 'high',
                'city': 'Pune',
                'state': 'Maharashtra',
                'address': 'School Approach Road, Baner',
                'pincode': '411045',
                'latitude': Decimal('18.520430'),
                'longitude': Decimal('73.856744'),
                'contact_number': '9988776655',
                'created_at': timezone.now() - timedelta(days=5),
            },
            {
                'title': 'Hospital waiting area cleanliness issue',
                'description': 'The waiting area at the district hospital is not maintained properly and needs immediate cleaning.',
                'department': departments[1],
                'assigned_to': created_users['district_officer_1'],
                'created_by': created_users['citizen_four'],
                'status': 'escalated',
                'urgency_level': 'high',
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'address': 'District Hospital, Anna Nagar',
                'pincode': '600040',
                'latitude': Decimal('13.082680'),
                'longitude': Decimal('80.270718'),
                'contact_number': '9871234560',
                'created_at': timezone.now() - timedelta(days=3),
            },
            {
                'title': 'Missing garbage collection in colony',
                'description': 'Garbage trucks have stopped visiting the colony for several days, creating hygiene concerns.',
                'department': departments[2],
                'assigned_to': created_users['staff_water'],
                'created_by': created_users['citizen_one'],
                'status': 'pending',
                'urgency_level': 'medium',
                'city': 'Delhi',
                'state': 'Delhi',
                'address': 'Garden Colony, Sector 15',
                'pincode': '110015',
                'latitude': Decimal('28.613939'),
                'longitude': Decimal('77.209021'),
                'contact_number': '9765432109',
                'created_at': timezone.now() - timedelta(days=1),
            },
            {
                'title': 'School roof leakage in classroom block',
                'description': 'Water is leaking through the roof and disrupting classes in the primary section.',
                'department': departments[5],
                'assigned_to': created_users['staff_education'],
                'created_by': created_users['citizen_two'],
                'status': 'in_progress',
                'urgency_level': 'high',
                'city': 'Lucknow',
                'state': 'Uttar Pradesh',
                'address': 'Govt. School, Hazratganj',
                'pincode': '226001',
                'latitude': Decimal('26.846695'),
                'longitude': Decimal('80.946167'),
                'contact_number': '9111222333',
                'created_at': timezone.now() - timedelta(days=4),
            },
            {
                'title': 'Broken bus shelter near market',
                'description': 'The bus shelter roof is broken and passengers wait in the rain.',
                'department': departments[3],
                'assigned_to': created_users['hod_transport'],
                'created_by': created_users['citizen_three'],
                'status': 'pending',
                'urgency_level': 'low',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Market Road, Andheri',
                'pincode': '400058',
                'latitude': Decimal('19.076090'),
                'longitude': Decimal('72.877426'),
                'contact_number': '9001122334',
                'created_at': timezone.now() - timedelta(days=2),
            },
            {
                'title': 'Transformer sparks near residential block',
                'description': 'A transformer is sparking dangerously close to residences and needs urgent inspection.',
                'department': departments[4],
                'assigned_to': created_users['staff_electricity'],
                'created_by': created_users['citizen_four'],
                'status': 'administrative_failure',
                'urgency_level': 'critical',
                'city': 'Ahmedabad',
                'state': 'Gujarat',
                'address': 'Residential Block B, Satellite',
                'pincode': '380015',
                'latitude': Decimal('23.022505'),
                'longitude': Decimal('72.571365'),
                'contact_number': '9888999888',
                'created_at': timezone.now() - timedelta(days=6),
            },
            {
                'title': 'Mobile vaccination camp request',
                'description': 'Residents are requesting a mobile vaccination camp for the area in the next week.',
                'department': departments[1],
                'assigned_to': created_users['hod_health'],
                'created_by': created_users['citizen_one'],
                'status': 'resolved',
                'urgency_level': 'medium',
                'city': 'Jaipur',
                'state': 'Rajasthan',
                'address': 'Sector 12 Community Hall',
                'pincode': '302001',
                'latitude': Decimal('26.912434'),
                'longitude': Decimal('75.787271'),
                'contact_number': '9666555444',
                'created_at': timezone.now() - timedelta(days=7),
            },
            {
                'title': 'Drain blockage causing flooding',
                'description': 'The drainage channel at the junction is blocked and water is flowing onto the road.',
                'department': departments[2],
                'assigned_to': created_users['district_officer_2'],
                'created_by': created_users['citizen_two'],
                'status': 'in_progress',
                'urgency_level': 'high',
                'city': 'Kolkata',
                'state': 'West Bengal',
                'address': 'Junction Road, Salt Lake',
                'pincode': '700091',
                'latitude': Decimal('22.572646'),
                'longitude': Decimal('88.363895'),
                'contact_number': '9555666777',
                'created_at': timezone.now() - timedelta(days=2),
            },
            {
                'title': 'Library books missing from school',
                'description': 'The school library reports several books are missing and the inventory is inconsistent.',
                'department': departments[5],
                'assigned_to': created_users['staff_education'],
                'created_by': created_users['citizen_three'],
                'status': 'pending',
                'urgency_level': 'low',
                'city': 'Bhopal',
                'state': 'Madhya Pradesh',
                'address': 'City School, New Market',
                'pincode': '462001',
                'latitude': Decimal('23.259933'),
                'longitude': Decimal('77.412613'),
                'contact_number': '9333444555',
                'created_at': timezone.now() - timedelta(days=1),
            },
            {
                'title': 'Public grievance about delayed permit processing',
                'description': 'A citizen reported that state permit processing has stalled without any update for several weeks.',
                'department': departments[0],
                'assigned_to': created_users['state_admin_demo'],
                'created_by': created_users['citizen_four'],
                'status': 'escalated',
                'urgency_level': 'medium',
                'city': 'Visakhapatnam',
                'state': 'Andhra Pradesh',
                'address': 'Government Office Complex',
                'pincode': '530001',
                'latitude': Decimal('17.686816'),
                'longitude': Decimal('83.218482'),
                'contact_number': '9444333222',
                'created_at': timezone.now() - timedelta(days=4),
            },
        ]

        for payload in complaint_samples:
            complaint, created = Complaint.objects.get_or_create(
                title=payload['title'],
                defaults={
                    'description': payload['description'],
                    'department': payload['department'],
                    'assigned_to': payload['assigned_to'],
                    'created_by': payload['created_by'],
                    'status': payload['status'],
                    'urgency_level': payload['urgency_level'],
                    'address': payload['address'],
                    'city': payload['city'],
                    'state': payload['state'],
                    'pincode': payload['pincode'],
                    'latitude': payload['latitude'],
                    'longitude': payload['longitude'],
                    'contact_number': payload['contact_number'],
                    'created_at': payload['created_at'],
                },
            )
            if not created:
                complaint.description = payload['description']
                complaint.department = payload['department']
                complaint.assigned_to = payload['assigned_to']
                complaint.created_by = payload['created_by']
                complaint.status = payload['status']
                complaint.urgency_level = payload['urgency_level']
                complaint.address = payload['address']
                complaint.city = payload['city']
                complaint.state = payload['state']
                complaint.pincode = payload['pincode']
                complaint.latitude = payload['latitude']
                complaint.longitude = payload['longitude']
                complaint.contact_number = payload['contact_number']
                complaint.created_at = payload['created_at']
                complaint.save()

            if not complaint.sla_deadline:
                complaint.sla_deadline = payload['created_at'] + timedelta(hours=complaint.department.sla_hours)
            if complaint.status in {'resolved', 'administrative_failure'}:
                complaint.resolved_at = complaint.created_at + timedelta(days=1)
            complaint.save()

            if complaint.id % 3 == 0:
                ComplaintComment.objects.get_or_create(
                    complaint=complaint,
                    author=complaint.created_by,
                    defaults={'comment_text': 'Thank you for logging this issue. We will follow up shortly.'},
                )
            if complaint.id % 4 == 0:
                ComplaintComment.objects.get_or_create(
                    complaint=complaint,
                    author=complaint.assigned_to,
                    defaults={'comment_text': 'We have reviewed the complaint and are working on a resolution plan.'},
                )

        escalations = [
            ('Public grievance about delayed permit processing', 'Escalated to the state admin because the request was pending beyond the SLA.', created_users['state_admin_demo']),
            ('Hospital waiting area cleanliness issue', 'Escalated after repeated follow-up was not completed in time.', created_users['hod_health']),
        ]
        for title, reason, escalated_to in escalations:
            complaint = Complaint.objects.filter(title=title).first()
            if complaint:
                EscalationLog.objects.get_or_create(
                    complaint=complaint,
                    defaults={
                        'escalated_to': escalated_to,
                        'reason': reason,
                    },
                )

        self.stdout.write(self.style.SUCCESS('Seeded demo data for departments, users, complaints, comments, and escalations.'))
