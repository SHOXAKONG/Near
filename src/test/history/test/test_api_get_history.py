import pytest
from src.test.base import TestBaseClass

@pytest.mark.django_db
class TestGetSearchHistoryAPI(TestBaseClass):
    def setup_method(self):
        self.user = self.base_user()
        self.url = '/uz/api/search-history/'
        self.client = self.base_client()
        self.format = self.base_format()
        self.auth = self.authenticate(self.user)
        self.category = self.create_category()
        self.search_history = self.create_search_history(user=self.user, category=self.category)

    def test_successful_get_list(self):
        response = self.client.get(self.url, format=self.format)

        assert response.status_code == 200
        assert isinstance(response.data, list) or 'results' in response.data
        assert any(item["id"] == self.search_history.id for item in response.data.get('results', response.data))
