import pytest
from django.urls import reverse
from rest_framework import status
from .factories import ComplaintFactory, DepartmentFactory

pytestmark = pytest.mark.django_db

@pytest.mark.integration
class TestComplaintAPI:
    def test_list_complaints_unauthenticated(self, api_client):
        """
        Verify that unauthenticated users cannot list complaints.
        """
        url = reverse('api_complaints')
        response = api_client.get(url)
        print("Unauthenticated Response:", response.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_complaints_citizen(self, authenticated_citizen_client, citizen_user):
        """
        Verify that citizens can only see their own complaints.
        """
        ComplaintFactory(created_by=citizen_user, title="My Complaint")
        ComplaintFactory(title="Other Complaint")  # Created by someone else

        url = reverse('api_complaints')
        response = authenticated_citizen_client.get(url)
        print("DEBUG IN TEST, citizen_user:", repr(citizen_user), "ROLE:", getattr(citizen_user, 'role', None))
        print("Citizen List Response:", response.data)
        assert response.status_code == status.HTTP_200_OK
        results = response.data.get('results', response.data.get('data', {}).get('complaints', []))
        assert len(results) == 1
        assert results[0]['title'] == "My Complaint"

    def test_create_complaint_citizen(self, authenticated_citizen_client):
        """
        Verify that a citizen can create a complaint successfully.
        """
        dept = DepartmentFactory(name="Roads")
        payload = {
            "title": "Pothole on Main St",
            "description": "Large pothole causing traffic issues.",
            "department": dept.id,
        }
        url = reverse('api_complaint_create')
        response = authenticated_citizen_client.post(url, data=payload, format='json')
        print("Create Response:", response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == "Pothole on Main St"
