import factory
from faker import Faker
from django.contrib.auth import get_user_model
from departments.models import Department
from complaints.models import Complaint
from api.constants import ROLE_CITIZEN, ROLE_STAFF

import random
from decimal import Decimal

fake = Faker('en_IN')
User = get_user_model()

class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    name = factory.LazyAttribute(lambda _: f"Dept of {fake.company()}")
    description = factory.Faker('catch_phrase')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = ROLE_CITIZEN

class CitizenFactory(UserFactory):
    role = ROLE_CITIZEN

class OfficerFactory(UserFactory):
    role = ROLE_STAFF
    department = factory.SubFactory(DepartmentFactory)

class ComplaintFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Complaint

    title = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    created_by = factory.SubFactory(CitizenFactory)
    department = factory.SubFactory(DepartmentFactory)
    status = 'pending'
    urgency_level = 'medium'
    address = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.Faker('state')
    pincode = factory.Faker('postcode')
    # India rough bounding box: Lat 8.0 to 37.0, Lon 68.0 to 97.0
    latitude = factory.LazyFunction(lambda: Decimal(str(round(random.uniform(8.0, 37.0), 6))))
    longitude = factory.LazyFunction(lambda: Decimal(str(round(random.uniform(68.0, 97.0), 6))))
