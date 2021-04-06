import pytest

from .base import TestBase


class TestDeleteMethod(TestBase):
    def setup_method(self):
        self.response = self.post_create_playlist(
            playlist_name="Playlist1",
            playlist_desc="Playlist1 description",
            is_playlist_public=True
        )

    def test_delete_unfollow_a_playlist_status_code(self):
        response = self.delete_unfollow_a_playlist(
            playlist_id=self.response.json()["id"]
        )

        assert response.status_code == 200
