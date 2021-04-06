import pytest

from .base import TestBase
from constants import ALBUM_ID_AKPH_AKKEZDET


class TestAuthentication(TestBase):
    @pytest.fixture()
    def create_playlist(self):
        print("*****SETUP*****")
        response = self.post_create_playlist(
            playlist_name="Beforehook playlist",
            playlist_desc="beforehook playlist description",
            is_playlist_public=True
        )
        yield response
        print("*****TEARDOWN*****")
        self.delete_unfollow_a_playlist(response.json()["id"])

    def test_get_playlist_by_id_status_code_empty_token(self, create_playlist):
        response = self.auth_get_playlist_by_id(
            playlist_id=create_playlist.json()["id"],
            bearer_token=""
        )

        assert response.status_code == 400

    def test_get_playlist_by_id_status_code_invalid_token(self, create_playlist):
        response = self.auth_get_playlist_by_id(
            playlist_id=create_playlist.json()["id"],
            bearer_token="SOMERANDOMStr123"
        )

        assert response.status_code == 401

    def test_get_playlist_by_id_status_code_no_token(self, create_playlist):
        response = self.auth_get_playlist_by_id(
            playlist_id=create_playlist.json()["id"]
        )

        assert response.status_code == 401
