from constants import TRACK_URI_AKPH_MIVEL_JATSZOL, TRACK_URI_NKS_FOLD
from base import TestBase
from support.assertions import assert_valid_schema
import pytest


class TestPostMethod(TestBase):
    @pytest.fixture()
    def create_playlist(self):
        print("*****SETUP*****")
        response = self.post_create_playlist(
            playlist_name="Beforehook playlist",
            playlist_desc="beforehook playlist description",
            playlist_is_public=True
        )
        yield response
        print("*****TEARDOWN*****")
        self.delete_unfollow_a_playlist(response.json()["id"])

    @pytest.mark.parametrize("playlist_name, playlist_desc, playlist_is_public",
                             [("Playlist1", "My First Playlist", True),
                              ("Playlist2", "My Second Playlist", False)])
    def test_post_create_playlist_status_code(self, playlist_name, playlist_desc, playlist_is_public):
        response = self.post_create_playlist(
            playlist_name=playlist_name,
            playlist_desc=playlist_desc,
            playlist_is_public=playlist_is_public
        )

        self.delete_unfollow_a_playlist(response.json()["id"])

        assert response.status_code == 201

    def test_post_create_playlist_status_code_negative(self):
        response = self.post_create_playlist(
            playlist_name=None
        )

        assert response.status_code == 400

    @pytest.mark.parametrize("playlist_name, playlist_desc, playlist_is_public",
                             [("Playlist1", "My First Playlist", True),
                              ("Playlist2", "My Second Playlist", False)])
    def test_post_create_playlist_properties(self, playlist_name, playlist_desc, playlist_is_public):
        response = self.post_create_playlist(
            playlist_name=playlist_name,
            playlist_desc=playlist_desc,
            playlist_is_public=playlist_is_public
        )

        self.delete_unfollow_a_playlist(response.json()["id"])

        assert response.json()["name"] == playlist_name
        assert response.json()[
            "description"] == playlist_desc
        assert response.json()["public"] == playlist_is_public

    def test_post_add_items_to_playlist_status_code(self, create_playlist):
        response = create_playlist

        response = self.post_add_items_to_playlist(
            playlist_id=response.json()["id"],
            track_uris=[TRACK_URI_AKPH_MIVEL_JATSZOL,
                        TRACK_URI_NKS_FOLD]
        )

        assert response.status_code == 201

    def test_post_add_items_to_playlist_schema(self, create_playlist):
        response = self.post_add_items_to_playlist(
            playlist_id=create_playlist.json()["id"],
            track_uris=[TRACK_URI_AKPH_MIVEL_JATSZOL,
                        TRACK_URI_NKS_FOLD]
        )

        assert_valid_schema(
            response.json(), 'add_item_to_playlist_schema.json')
