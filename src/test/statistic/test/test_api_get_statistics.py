import pytest
from src.test.base import TestBaseClass
from src.apps.history.models import SearchHistory
# from datetime import date

@pytest.mark.django_db
class TestStatisticsAPI(TestBaseClass):

    def setup_method(self):
        self.user = self.base_user()
        self.client = self.base_client()
        self.format = self.base_format()
        self.auth = self.authenticate(self.user)
        self.category = self.create_category()
        self.url_prefix = '/uz/api/statistics'

    def create_search_history(self, count=3):
        for _ in range(count):
            SearchHistory.objects.create(
                user=self.user,
                category=self.category,
                latitude=41.3111,
                longitude=69.2797,
            )

    def test_category_stat(self):
        self.create_search_history()
        url = f"{self.url_prefix}/by-category/"
        response = self.client.get(url, format=self.format)
        assert response.status_code == 200
        assert isinstance(response.data, dict)
        assert 'results' in response.data
        assert isinstance(response.data['results'], list)
        assert len(response.data['results']) > 0
        assert 'category_id' in response.data['results'][0]
        assert 'category_name' in response.data['results'][0]
        assert 'search_count' in response.data['results'][0]

    def test_active_user_stat(self):
        self.create_search_history()
        url = f"{self.url_prefix}/active-users/"
        response = self.client.get(url, format=self.format)
        assert response.status_code == 200
        assert isinstance(response.data, dict)
        assert 'results' in response.data
        assert isinstance(response.data['results'], list)
        assert len(response.data['results']) > 0
        assert 'user_id' in response.data['results'][0]
        assert 'first_name' in response.data['results'][0]
        assert 'total_searches' in response.data['results'][0]

    def test_daily_stat(self):
        self.create_search_history()
        url = f"{self.url_prefix}/daily-searches/"
        response = self.client.get(url, format=self.format)

        assert response.status_code == 200
        assert isinstance(response.data, dict)
        assert 'results' in response.data
        assert isinstance(response.data['results'], list)
        if len(response.data['results']) > 0:
            assert 'date' in response.data['results'][0]
            assert 'search_count' in response.data['results'][0]

    def test_monthly_stat(self):
        self.create_search_history()
        url = f"{self.url_prefix}/monthly-summary/"
        response = self.client.get(url, format=self.format)
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) > 0
        assert 'month' in response.data[0]
        assert 'user_registrations' in response.data[0]
        assert 'category_searches' in response.data[0]

    def test_user_search_history(self):
        self.create_search_history(5)
        url = f"{self.url_prefix}/search-history-users/"
        response = self.client.get(url, format=self.format)
        assert response.status_code == 200
        assert isinstance(response.data, dict)
        assert 'results' in response.data
        assert isinstance(response.data['results'], list)
        assert len(response.data['results']) > 0