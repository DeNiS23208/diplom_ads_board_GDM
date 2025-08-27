import pytest

@pytest.mark.django_db
def test_create_ad_requires_auth(api_client, category):
    payload = {'title': 'test', 'description': 'd', 'price': 100, 'category_id': category.id}
    resp = api_client.post('/api/ads/', payload, format='json')
    assert resp.status_code == 401