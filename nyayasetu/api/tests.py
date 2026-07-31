from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from departments.models import Department
import json

User = get_user_model()

class ApiIntegrationTests(TestCase):
  def setUp(self):
    self.client = Client()
    # Create test department
    self.dept = Department.objects.create(
      name="Test Electricity Dept",
      description="Testing depts",
      sla_hours=24,
      transparency_score=100.0
    )
    # Create test user
    self.user = User.objects.create_user(
      username="testcitizen",
      first_name="Test",
      last_name="Citizen",
      email="test@citizen.gov.in",
      password="password123",
      role="citizen"
    )

  def test_get_session_unauthenticated(self):
    """Test session check returns false when not logged in."""
    response = self.client.get(reverse('api_session'))
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content)
    self.assertFalse(data['isAuthenticated'])
    self.assertIn('csrfToken', data)

  def test_login_invalid_credentials(self):
    """Test login fails with incorrect password."""
    payload = {
      "username": "testcitizen",
      "password": "wrongpassword"
    }
    response = self.client.post(
      reverse('api_login'),
      data=json.dumps(payload),
      content_type="application/json"
    )
    self.assertEqual(response.status_code, 401)
    data = json.loads(response.content)
    self.assertIn('error', data)

  def test_get_departments(self):
    """Test fetching list of departments."""
    response = self.client.get(reverse('api_departments'))
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.content)
    self.assertIn('departments', data)
    self.assertEqual(len(data['departments']), 1)
    self.assertEqual(data['departments'][0]['name'], "Test Electricity Dept")
