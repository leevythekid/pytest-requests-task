from base import TestBase
import pytest


class TestDeleteMethod(TestBase):
    @pytest.fixture(scope='module')
    def create_playlist(self):
        print("*****SETUP*****")
        response = self.post_create_playlist(
            playlist_name="Playlist1",
            playlist_desc="Playlist1 description",
            playlist_is_public=True
        )
        yield response

    def test_delete_unfollow_a_playlist_status_code(self, create_playlist):
        response = create_playlist

        response = self.delete_unfollow_a_playlist(
            playlist_id=response.json()["id"]
        )

        assert response.status_code == 200
