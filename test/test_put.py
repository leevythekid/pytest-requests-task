from base import TestBase
import pytest


class TestPutMethod(TestBase):
    @pytest.fixture(scope='module')
    def create_playlist(self):
        print("*****SETUP*****")
        response = self.post_create_playlist(
            playlist_name="Playlist1",
            playlist_desc="Playlist1 description",
            playlist_is_public=True
        )
        yield response
        print("*****TEARDOWN*****")
        self.delete_unfollow_a_playlist(response.json()["id"])

    def test_update_playlist_details_status_code(self, create_playlist):
        response = self.put_update_playlist_details(
            playlist_id=create_playlist.json()["id"],
            new_playlist_name="WfH updated name",
            new_playlist_desc="updated description",
            new_playlist_is_public=True
        )

        assert response.status_code == 200

    def test_update_playlist_details_properties(self, create_playlist):
        self.put_update_playlist_details(
            playlist_id=create_playlist.json()["id"],
            new_playlist_name="updated updated name",
            new_playlist_desc="updated updated description",
            new_playlist_is_public=True
        )

        response = self.get_playlist_by_id(create_playlist.json()["id"])

        assert response.json()["name"] == "updated updated name"
        assert response.json()["description"] == "updated updated description"
        assert response.json()["public"] == True
