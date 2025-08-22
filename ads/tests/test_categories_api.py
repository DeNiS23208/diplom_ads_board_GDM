import pytest

@pytest.mark.django_db
def test_list_categories(api_client):
    resp = api_client.get('/api/categories/')
    assert resp.status_code == 200

@pytest.mark.django_db
def test_create_category_requires_auth(api_client):
    resp = api_client.post('/api/categories/', {'name': 'Электроника'})
    assert resp.status_code in (401, 403)
