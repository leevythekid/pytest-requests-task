import pytest

from .base import TestBase
from constants import ALBUM_ID_AKPH_AKKEZDET, EXPIRED_TOKEN


class TestAuthorization(TestBase):
    @pytest.fixture(scope="class")
    def create_playlist(self):
        print("*****SETUP*****")
        response = self.post_create_playlist(
            playlist_name="Playlist_Authorization",
            playlist_desc="beforehook playlist description",
            is_playlist_public=True
        )
        yield response
        print("*****TEARDOWN*****")
        self.delete_unfollow_a_playlist(response.json()["id"])

    @pytest.mark.parametrize(
        "bearer_token, expected_status_code",
        [
            ("", 400),
            ("SOMERANDOMStr123", 401),
            (EXPIRED_TOKEN, 401),
            (None, 401)
        ]
    )
    def test_get_playlist_by_id_status_code(self, create_playlist, bearer_token, expected_status_code):
        response = self.get_playlist_by_id(
            playlist_id=create_playlist.json()["id"],
            bearer_token=bearer_token
        )
        if bearer_token == None:
            print(bearer_token)
            print(response.json())
        assert (
            response.status_code == expected_status_code
        ), f"Status code is expected to be: {expected_status_code}."
