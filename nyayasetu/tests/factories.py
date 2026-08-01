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
    description = factory.LazyFunction(lambda: fake.catch_phrase())

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyFunction(lambda: fake.user_name())
    email = factory.LazyFunction(lambda: fake.email())
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    role = ROLE_CITIZEN

class CitizenFactory(UserFactory):
    role = ROLE_CITIZEN

class OfficerFactory(UserFactory):
    role = ROLE_STAFF
    department = factory.SubFactory(DepartmentFactory)

class ComplaintFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Complaint

    title = factory.LazyFunction(lambda: fake.sentence())
    description = factory.LazyFunction(lambda: fake.paragraph())
    created_by = factory.SubFactory(CitizenFactory)
    department = factory.SubFactory(DepartmentFactory)
    status = 'pending'
    urgency_level = 'medium'
    address = factory.LazyFunction(lambda: fake.street_address())
    city = factory.LazyFunction(lambda: fake.city())
    state = factory.LazyFunction(lambda: fake.state())
    pincode = factory.LazyFunction(lambda: fake.postcode())
    # India rough bounding box: Lat 8.0 to 37.0, Lon 68.0 to 97.0
    latitude = factory.LazyFunction(lambda: Decimal(str(round(random.uniform(8.0, 37.0), 6))))
    longitude = factory.LazyFunction(lambda: Decimal(str(round(random.uniform(68.0, 97.0), 6))))
