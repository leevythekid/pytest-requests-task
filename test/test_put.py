import pytest

from .base import TestBase
from constants import OAUTH_TOKEN


class TestPutMethod(TestBase):
    @pytest.fixture(scope="class")
    def create_playlist(self):
        print("*****SETUP*****")
        response = self.post_create_playlist(
            playlist_name="Playlist_Put",
            playlist_desc="Playlist1 description",
            is_playlist_public=False
        )
        yield response
        print("*****TEARDOWN*****")
        self.delete_unfollow_a_playlist(response.json()["id"])

    def test_update_playlist_details_status_code(self, create_playlist):
        response = self.put_update_playlist_details(
            playlist_id=create_playlist.json()["id"],
            new_playlist_name="Playlist_Put_1",
            new_playlist_desc="updated description",
            is_new_playlist_public=True
        )

        assert (
            response.status_code == 200
        ), f"Status code is expected to be: 200."

    def test_update_playlist_name(self, create_playlist):
        self.put_update_playlist_details(
            playlist_id=create_playlist.json()["id"],
            new_playlist_name="Playlist_Put_2"
        )

        response = self.get_playlist_by_id(
            create_playlist.json()["id"], OAUTH_TOKEN)

        assert (
            response.json()["name"] == "Playlist_Put_2"
        ), f"Name is expected to be: 'Playlist_Put_2'."

    def test_update_playlist_description(self, create_playlist):
        self.put_update_playlist_details(
            playlist_id=create_playlist.json()["id"],
            new_playlist_desc="updated description"
        )

        response = self.get_playlist_by_id(
            create_playlist.json()["id"], OAUTH_TOKEN)

        assert (
            response.json()["description"] == "updated description"
        ), f"Description is expected to be: 'updated description'."

    def test_update_playlist_visibility(self, create_playlist):
        self.put_update_playlist_details(
            playlist_id=create_playlist.json()["id"],
            is_new_playlist_public=True
        )

        response = self.get_playlist_by_id(
            create_playlist.json()["id"], OAUTH_TOKEN)

        assert (
            response.json()["public"] == True
        ),  f"Visibility is expected to be: True."
