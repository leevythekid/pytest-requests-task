from base import TestBase
import pytest


class TestGetMethod(TestBase):
    def test_get_status_code_album(self):
        response = self.get_album_by_id(album_id="16tDx6tKDmxMfNQyhfsaIg")
        # print(response.json())
        assert response.status_code == 200
