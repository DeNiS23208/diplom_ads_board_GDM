import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from ads.models import Category, Ad


@pytest.fixture
def api_client():

    return APIClient()


def _create_user(**kwargs):

    User = get_user_model()
    defaults = dict(email='user@example.com', password='P4$$w0rd')
    defaults.update(kwargs)


    if any(f.name == 'username' for f in User._meta.get_fields()) and 'username' not in defaults:
        defaults['username'] = defaults['email'].split('@')[0]

    return User.objects.create_user(**defaults)


@pytest.fixture
def user(db):
    return _create_user(email='user1@example.com')


@pytest.fixture
def staff_user(db):
    u = _create_user(email='staff@example.com')
    u.is_staff = True
    u.save(update_fields=['is_staff'])
    return u


@pytest.fixture
def category(db):
    return Category.objects.create(name='Тест')


@pytest.fixture
def ad(db, user, category):
    return Ad.objects.create(
        title='test',
        description='desc',
        price=100,
        owner=user,
        category=category
    )
