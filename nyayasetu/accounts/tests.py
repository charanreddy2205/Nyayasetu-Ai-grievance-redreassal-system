from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from complaints.models import Complaint, ComplaintComment
from departments.models import Department
from escalation.models import EscalationLog

User = get_user_model()


class SeedDemoDataCommandTests(TestCase):
    def test_seed_demo_data_creates_departments_users_and_complaints(self):
        call_command('seed_demo_data')

        self.assertGreaterEqual(Department.objects.count(), 6)
        self.assertGreaterEqual(User.objects.filter(role='state_admin').count(), 1)
        self.assertGreaterEqual(User.objects.filter(role='district_officer').count(), 2)
        self.assertGreaterEqual(Complaint.objects.count(), 12)
        self.assertGreaterEqual(
            Complaint.objects.filter(status='administrative_failure').count(),
            1,
        )
        self.assertGreaterEqual(ComplaintComment.objects.count(), 3)
        self.assertGreaterEqual(EscalationLog.objects.count(), 2)
