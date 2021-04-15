import pytest

from .base import TestBase
from constants import (
    TRACK_URI_AKPH_MIVEL_JATSZOL,
    TRACK_URI_NKS_FOLD,
    TRACK_URI_QUEEN_UNDER_PRESSURE,
    TRACK_URI_PANTERA_WALK,
    PLAYLIST_ID_QUEEN_LIVE
)


class TestDeleteMethod(TestBase):
    def setup_method(self):
        self.response = self.post_create_playlist(
            playlist_name="Playlist_Delete",
            playlist_desc="Playlist1 description",
            is_playlist_public=True
        )
        self.post_add_items_to_playlist(self.response.json()["id"], [
            TRACK_URI_AKPH_MIVEL_JATSZOL,
            TRACK_URI_NKS_FOLD,
            TRACK_URI_AKPH_MIVEL_JATSZOL,
            TRACK_URI_QUEEN_UNDER_PRESSURE,
            TRACK_URI_AKPH_MIVEL_JATSZOL
        ])

    def teardown_method(self):
        self.delete_unfollow_a_playlist(self.response.json()["id"])

    def test_delete_unfollow_a_playlist_status_code(self):
        response = self.delete_unfollow_a_playlist(
            playlist_id=self.response.json()["id"]
        )

        assert (
            response.status_code == 200
        ), f"Status code is expected to be: 200."

    def test_delete_items_from_playlist(self):
        self.delete_items_from_playlist(
            playlist_id=self.response.json()["id"],
            tracks=[{"uri": TRACK_URI_AKPH_MIVEL_JATSZOL},
                    {"uri": TRACK_URI_NKS_FOLD}]
        )

        self.assert_playlist_contains_tracks(
            self.response.json()["id"],
            [{"uri": TRACK_URI_AKPH_MIVEL_JATSZOL}, {"uri": TRACK_URI_NKS_FOLD}]
        )

    def test_delete_items_from_playlist_with_position(self):
        self.delete_items_from_playlist(
            playlist_id=self.response.json()["id"],
            tracks=[{"uri": TRACK_URI_AKPH_MIVEL_JATSZOL, "positions": [0, 2, 4]}]
        )

        self.assert_playlist_contains_tracks(
            self.response.json()["id"],
            [{"uri": TRACK_URI_AKPH_MIVEL_JATSZOL}]
        )

    def test_delete_non_existing_items_from_playlist_without_position(self):
        response = self.delete_items_from_playlist(
            playlist_id=self.response.json()["id"],
            tracks=[{"uri": TRACK_URI_PANTERA_WALK}]
        )

        assert (
            response.status_code == 200
        ), f"Status code is expected to be: 200."

    def test_delete_non_existing_items_from_playlist_with_positon(self):
        response = self.delete_items_from_playlist(
            playlist_id=self.response.json()["id"],
            tracks=[{"uri": TRACK_URI_PANTERA_WALK, "positions": [3]}]
        )

        assert (
            response.status_code == 400
        ), f"Status code is expected to be: 400."

    def test_delete_items_from_not_owned_playlist(self):
        response = self.delete_items_from_playlist(
            playlist_id=PLAYLIST_ID_QUEEN_LIVE,
            tracks=[{"uri": TRACK_URI_QUEEN_UNDER_PRESSURE}]
        )

        assert (
            response.status_code == 403
        ), f"Status code is expected to be: 403."

    def test_delete_items_from_non_existing_playlist(self):
        response = self.delete_items_from_playlist(
            playlist_id="nonExistingPlaylist",
            tracks=[{"uri": TRACK_URI_AKPH_MIVEL_JATSZOL}]
        )

        assert (
            response.status_code == 404
        ), f"Status code is expected to be: 404."
