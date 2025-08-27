import pytest
from ads.models import Ad, Category

@pytest.mark.django_db
def test_ads_pagination_page_size(api_client, user, django_assert_num_queries):
    cat = Category.objects.create(name='Тест')
    for i in range(7):
        Ad.objects.create(title=f't{i}', description='d', price=100+i, owner=user, category=cat)
    resp = api_client.get('/api/ads/?page=1')
    assert resp.status_code == 200
    assert len(resp.json()['results']) == 4  # PAGE_SIZE=4

@pytest.mark.django_db
def test_search_by_title(api_client, user, category):
    Ad.objects.create(title='iPhone 15', description='d', price=1, owner=user, category=category)
    Ad.objects.create(title='Samsung', description='d', price=2, owner=user, category=category)
    resp = api_client.get('/api/ads/?search=iphone')
    assert resp.status_code == 200
    titles = [x['title'].lower() for x in resp.json()['results']]
    assert 'iphone 15' in titles
