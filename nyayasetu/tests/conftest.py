import pytest
from rest_framework.test import APIClient
from .factories import CitizenFactory, OfficerFactory

@pytest.fixture
def citizen_user(db):
    return CitizenFactory()

@pytest.fixture
def officer_user(db):
    return OfficerFactory()

@pytest.fixture
def api_client():
    """
    Provides an unauthenticated API client.
    """
    return APIClient()

@pytest.fixture
def authenticated_citizen_client(api_client, citizen_user):
    """
    Provides an API client authenticated as a standard citizen.
    """
    api_client.force_authenticate(user=citizen_user)
    return api_client

@pytest.fixture
def authenticated_officer_client(api_client, officer_user):
    """
    Provides an API client authenticated as a departmental officer.
    """
    api_client.force_authenticate(user=officer_user)
    return api_client
