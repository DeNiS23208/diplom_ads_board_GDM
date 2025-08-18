import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker
from django.contrib.auth import get_user_model
from ads.models import Ad, Category

User = get_user_model()

@pytest.mark.django_db
def test_create_ad_requires_auth():
    client = APIClient()
    url = reverse('ad-list')
    resp = client.post(url, {'title': 'test', 'description': 'd', 'is_active': True})
    assert resp.status_code == 401

@pytest.mark.django_db
def test_owner_can_create_and_update_ad():
    user = User.objects.create_user(username='u1', password='p1')
    cat = baker.make(Category)
    client = APIClient()
    # login via JWT
    from rest_framework_simplejwt.tokens import RefreshToken
    access = RefreshToken.for_user(user).access_token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    # create
    url = reverse('ad-list')
    resp = client.post(url, {
        'title': 'Продам велик',
        'description': 'отличный',
        'is_active': True,
        'category_id': cat.id
    }, format='json')
    assert resp.status_code == 201
    ad_id = resp.data['id']

    # update own
    url = reverse('ad-detail', args=[ad_id])
    resp = client.patch(url, {'title': 'Продам велосипед'}, format='json')
    assert resp.status_code == 200
    assert resp.data['title'] == 'Продам велосипед'

@pytest.mark.django_db
def test_non_owner_cannot_update():
    owner = User.objects.create_user(username='owner', password='p1')
    other = User.objects.create_user(username='other', password='p2')
    cat = baker.make(Category)
    ad = baker.make(Ad, owner=owner, category=cat, title='X')

    client = APIClient()
    from rest_framework_simplejwt.tokens import RefreshToken
    token = RefreshToken.for_user(other).access_token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    url = reverse('ad-detail', args=[ad.id])
    resp = client.patch(url, {'title': 'Y'}, format='json')
    assert resp.status_code in (403, 401)

@pytest.mark.django_db
def test_filter_by_price_range():
    u = User.objects.create_user(username='u', password='p')
    cat = baker.make(Category)
    baker.make(Ad, owner=u, category=cat, price=1000)
    baker.make(Ad, owner=u, category=cat, price=50000)

    client = APIClient()
    url = reverse('ad-list') + '?price_min=2000&price_max=40000'
    resp = client.get(url)
    assert resp.status_code == 200
    assert len(resp.data['results']) == 0 or all(2000 <= (a.get('price') or 0) <= 40000 for a in resp.data['results'])
