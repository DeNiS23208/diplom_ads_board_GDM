import pytest
from rest_framework.test import APIClient
from ads.models import Ad


@pytest.mark.django_db
def test_approve_requires_staff(api_client, user, staff_user, ad):
    client = APIClient()
    client.force_authenticate(user=user)
    r1 = client.post(f'/api/ads/{ad.id}/approve/')
    assert r1.status_code in (403, 401)

    client.force_authenticate(user=staff_user)
    r2 = client.post(f'/api/ads/{ad.id}/approve/')
    assert r2.status_code == 200
    ad.refresh_from_db()
    assert ad.status == Ad.Status.PUBLISHED
