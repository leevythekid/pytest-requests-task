from constants import TRACK_URI_AKPH_MIVEL_JATSZOL, TRACK_URI_NKS_FOLD
from base import TestBase
from support.assertions import assert_valid_schema
import pytest


class TestPostMethod(TestBase):
    @pytest.fixture(scope="module")
    def create_playlist(self):
        # print("*****SETUP*****")
        response = self.post_create_playlist(
            playlist_name="Playlist1",
            playlist_desc="Playlist1 description",
            playlist_is_public=True
        )
        yield response
        # print("*****TEARDOWN*****")
        self.delete_unfollow_a_playlist(response.json()["id"])

    def test_post_create_playlist_status_code(self, create_playlist):
        response = create_playlist

        assert response.status_code == 201

    def test_post_create_playlist_properties(self, create_playlist):
        response = create_playlist

        assert response.json()["name"] == "Playlist1"
        assert response.json()[
            "description"] == "Playlist1 description"
        assert response.json()["public"] == True

    def test_post_add_items_to_playlist(self, create_playlist):
        response = create_playlist

        response = self.post_add_items_to_playlist(
            playlist_id=response.json()["id"],
            track_uris=[TRACK_URI_AKPH_MIVEL_JATSZOL,
                        TRACK_URI_NKS_FOLD]
        )

        assert response.status_code == 201

    def test_add_items_to_playlist_schema(self, create_playlist):
        response = self.post_add_items_to_playlist(
            playlist_id=create_playlist.json()["id"],
            track_uris=[TRACK_URI_AKPH_MIVEL_JATSZOL,
                        TRACK_URI_NKS_FOLD]
        )

        assert_valid_schema(
            response.json(), 'playlist_add_item_to_playlist_schema.json')
