import pytest

from .base import TestBase
from constants import USER_ID, OAUTH_TOKEN

_ERROR_INVALID_USERNAME = "Invalid username"


class TestCreatePlaylist(TestBase):
    def setup_method(self):
        response = self.get_list_of_current_users_playlist()

        if len(response["items"]) > 0:
            for playlist in response["items"]:
                if playlist["owner"]["id"] == USER_ID:
                    self.unfollow_a_playlist(playlist["id"])

    # def teardown_method(self):
    # check if the user owns any playlist
    #    pass

    @pytest.mark.parametrize(
        "token, user_id, playlist_name, is_public, is_collaborative, playlist_description, status_code, error_message",
        [
        (OAUTH_TOKEN, None, "playlist_1", None, None, "desc", 404, "Invalid username"),
        (OAUTH_TOKEN, None, "playlist_1", True, True, {}, 404, "Invalid username"),
        (OAUTH_TOKEN, ["invalid_user_id"], None, None, "no", None, 404, "Invalid username"),
        (OAUTH_TOKEN, ["invalid_user_id"], {"invalid": "name"}, None, True, None, 404, "Invalid username")
        ]
    )
    def test_invalid_user_id(self, token, user_id, playlist_name, is_public, is_collaborative, playlist_description, status_code, error_message):
        response = self.post_create_playlist(
            status_code=status_code,
            token=token,
            user_id=user_id,
            playlist_name=playlist_name,
            is_public=is_public,
            is_collaborative=is_collaborative,
            playlist_description=playlist_description,
        )

        self.assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == error_message
        ), f"Response message is: {response['error']['message']}, should be: '{error_message}'."

        self.assert_current_user_owns_playlist(0)

    def test_TC15_create_playlist(self):
        response = self.post_create_playlist(
            status_code=201,
            token=OAUTH_TOKEN,
            user_id=USER_ID,
            playlist_name="name"
        )

        self.assert_valid_schema(response, 'playlist_schema.yml')

        assert (response["name"] == "name")
        assert (response["public"] == True)
        assert (response["collaborative"] == False)
        assert (response["description"] == None)

        response_playlists = self.get_list_of_current_users_playlist()

        playlists = self.assert_current_user_owns_playlist(1)

        assert (playlists[0]["id"] == response["id"])
        assert (playlists[0]["name"] == response["name"])