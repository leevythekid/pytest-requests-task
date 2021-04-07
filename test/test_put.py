import pytest

from .base import TestBase


class TestPutMethod(TestBase):
    def setup_class(self):
        print("*****SETUP*****")
        self.response = self.post_create_playlist(
            self=self,
            playlist_name="Playlist1",
            playlist_desc="Playlist1 description",
            is_playlist_public=False
        )

    def teardown_class(self):
        print("*****TEARDOWN*****")
        self.delete_unfollow_a_playlist(self.response.json()["id"])

    def test_update_playlist_details_status_code(self):
        response = self.put_update_playlist_details(
            playlist_id=self.response.json()["id"],
            new_playlist_name="WfH updated name",
            new_playlist_desc="updated description",
            is_new_playlist_public=True
        )

        assert response.status_code == 200

    def test_update_playlist_details_property_name(self):
        self.put_update_playlist_details(
            playlist_id=self.response.json()["id"],
            new_playlist_name="updated name",
        )

        response = self.get_playlist_by_id(self.response.json()["id"])

        assert response.json()["name"] == "updated name"

    def test_update_playlist_details_property_description(self):
        self.put_update_playlist_details(
            playlist_id=self.response.json()["id"],
            new_playlist_desc="updated description",
        )

        response = self.get_playlist_by_id(self.response.json()["id"])

        assert response.json()["description"] == "updated description"

    def test_update_playlist_details_property_visibility(self):
        self.put_update_playlist_details(
            playlist_id=self.response.json()["id"],
            is_new_playlist_public=True
        )

        response = self.get_playlist_by_id(self.response.json()["id"])

        assert response.json()["public"] == True
