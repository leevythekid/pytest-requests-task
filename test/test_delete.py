import pytest

from .base import TestBase
from constants import TRACK_URI_AKPH_MIVEL_JATSZOL, TRACK_URI_NKS_FOLD


class TestDeleteMethod(TestBase):
    def setup_method(self):
        self.response = self.post_create_playlist(
            playlist_name="Playlist1",
            playlist_desc="Playlist1 description",
            is_playlist_public=True
        )
        self.post_add_items_to_playlist(self.response.json()["id"], [
                                        TRACK_URI_AKPH_MIVEL_JATSZOL])

    def teardown_method(self):
        self.delete_unfollow_a_playlist(self.response.json()["id"])

    def test_delete_unfollow_a_playlist_status_code(self):
        response = self.delete_unfollow_a_playlist(
            playlist_id=self.response.json()["id"]
        )

        assert response.status_code == 200

    def test_delete_remove_items_from_playlist(self):
        response = self.delete_remove_items_from_playlist(
            self.response.json()["id"],
            [{"uri": TRACK_URI_AKPH_MIVEL_JATSZOL, "positions": [0]}]
        )

        assert response.status_code == 200

    def test_delete_remove_items_from_playlist_non_existing(self):
        response = self.delete_remove_items_from_playlist(
            self.response.json()["id"],
            [{"uri": TRACK_URI_NKS_FOLD}]
        )

        assert response.status_code == 200
