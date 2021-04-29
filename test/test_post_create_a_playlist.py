import pytest

from .assertions import (
    assert_compare_playlists,
    assert_current_user_owns_playlist,
    assert_valid_schema
)
from .base import TestBase
from constants import USER_ID, OAUTH_TOKEN

_ERROR_INVALID_USERNAME = "Invalid username"
_ERROR_COLLABORATIVE = "Collaborative playlists can only be private."
_ERROR_INSUFFICIENT_SCOPE = "Insufficient client scope"
_ERROR_PARSING = "Error parsing JSON."
_ERROR_INVALID_TOKEN = "Invalid access token"
_ERROR_NO_TOKEN = "No token provided"

_INVALID_TOKEN = "x"
_INVALID_USER_ID = ["invalid"]
_INVALID_PLAYLIST_NAME = {"name": "playlist_name"}
_INVALID_VISIBILITY = "yes"
_INVALID_COLLABORATIVE = "no"
_INVALID_DESCRIPTION = ["description"]

_VALID_PLAYLIST_NAME = "playlist_name"
_VALID_VISIBILITY = True
_VALID_COLLABORATIVE = False
_VALID_DESCRIPTION = "playlist_desc"


class TestCreatePlaylist(TestBase):

    @pytest.fixture()
    def remove_owned_playlists(self):
        print("****SETUP****")
        yield 0
        print("****TEARDOWN****")
        owned_playlists = self.get_owned_playlists_of_current_user()
        for playlist in owned_playlists:
            self.unfollow_a_playlist(playlist_id=playlist["id"])

    @pytest.mark.parametrize(
        "token, user_id, playlist_name, is_public, is_collaborative, playlist_description, status_code, error_message",
        [
            (OAUTH_TOKEN, None, "playlist_1", None,
             None, "desc", 404, _ERROR_INVALID_USERNAME),
            (OAUTH_TOKEN, None, "playlist_1", True,
             True, {}, 404, _ERROR_INVALID_USERNAME),
            (OAUTH_TOKEN, ["invalid_user_id"], None, None,
             "no", None, 404, _ERROR_INVALID_USERNAME),
            (OAUTH_TOKEN, ["invalid_user_id"], {
             "invalid": "name"}, None, True, None, 404, _ERROR_INVALID_USERNAME)
        ]
    )
    def test_invalid_user_id(self, remove_owned_playlists, token, user_id, playlist_name, is_public, is_collaborative, playlist_description, status_code, error_message):
        response = self.post_create_playlist(
            status_code=status_code,
            token=token,
            user_id=user_id,
            playlist_name=playlist_name,
            is_public=is_public,
            is_collaborative=is_collaborative,
            playlist_description=playlist_description,
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == error_message
        ), f"Response message is: {response['error']['message']}, should be: '{error_message}'."

        assert_current_user_owns_playlist(0)

    @pytest.mark.parametrize(
        "token, user_id, playlist_name, is_public, is_collaborative, playlist_description, status_code, error_message",
        [
            (OAUTH_TOKEN, USER_ID, None, _INVALID_VISIBILITY,
             None, _INVALID_DESCRIPTION, 400, _ERROR_PARSING),
            (_INVALID_TOKEN, None, _INVALID_PLAYLIST_NAME,
             None, None, None, 401, _ERROR_INVALID_TOKEN),
            (_INVALID_TOKEN, _INVALID_USER_ID, _INVALID_PLAYLIST_NAME, _INVALID_VISIBILITY,
             _INVALID_COLLABORATIVE, _INVALID_DESCRIPTION, 401, _ERROR_INVALID_TOKEN),
            (_INVALID_TOKEN, _INVALID_USER_ID, _VALID_PLAYLIST_NAME, _VALID_VISIBILITY,
             _INVALID_COLLABORATIVE, _VALID_DESCRIPTION, 401, _ERROR_INVALID_TOKEN),
            (_INVALID_TOKEN, USER_ID, None, None, _VALID_COLLABORATIVE,
             _VALID_DESCRIPTION, 401, _ERROR_INVALID_TOKEN),
            (None, None, None, None, _INVALID_COLLABORATIVE,
             _INVALID_DESCRIPTION, 401, _ERROR_NO_TOKEN),
            (None, None, _INVALID_PLAYLIST_NAME, _INVALID_VISIBILITY,
             _VALID_COLLABORATIVE, _VALID_DESCRIPTION, 401, _ERROR_NO_TOKEN),
            (None, _INVALID_USER_ID, None, _VALID_VISIBILITY,
             None, _INVALID_DESCRIPTION, 401, _ERROR_NO_TOKEN),
            (None, USER_ID, _INVALID_PLAYLIST_NAME, _VALID_VISIBILITY,
             _INVALID_COLLABORATIVE, None, 401, _ERROR_NO_TOKEN),
            (None, USER_ID, _VALID_PLAYLIST_NAME, _INVALID_VISIBILITY,
             _VALID_COLLABORATIVE, None, 401, _ERROR_NO_TOKEN)
        ]
    )
    def test_invalid_properties(self, remove_owned_playlists, token, user_id, playlist_name, is_public, is_collaborative, playlist_description, status_code, error_message):
        response = self.post_create_playlist(
            status_code=status_code,
            token=token,
            user_id=user_id,
            playlist_name=playlist_name,
            is_public=is_public,
            is_collaborative=is_collaborative,
            playlist_description=playlist_description,
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == error_message
        ), f"Response message is: {response['error']['message']}, should be: '{error_message}'."

        assert_current_user_owns_playlist(0)

    def test_TC15_create_playlist_with_required_fields(self, remove_owned_playlists):
        response = self.post_create_playlist(
            token=OAUTH_TOKEN,
            user_id=USER_ID,
            playlist_name="name"
        )

        assert_valid_schema(response, 'playlist_object_schema.yml')

        assert (
            response["name"] == "name"
        ), f"Response 'name' is: {response['name']}, should be: 'name'."
        assert (
            response["public"] == True
        ), f"Response 'public' is: {response['public']}, should be: 'True'."
        assert (
            response["collaborative"] == False
        ), f"Response 'collaborative' is: {response['collaborative']}, should be: 'False'."
        assert (
            response["description"] == None
        ), f"Response 'description' is: {response['description']}, should be: None."

        assert_current_user_owns_playlist(1)

        owned_playlist = self.get_owned_playlists_of_current_user()[0]

        assert_compare_playlists(
            owned_playlist, response, ["description",
                                       "followers", "snapshot_id", "tracks"]
        )

    @pytest.mark.parametrize(
        "is_public, is_collaborative",
        [
            (True, False),
            (False, True),
            (False, False)
        ]
    )
    def test_TC16_create_playlist_with_all_fields(self, remove_owned_playlists, is_public, is_collaborative):
        response = self.post_create_playlist(
            token=OAUTH_TOKEN,
            user_id=USER_ID,
            playlist_name="name",
            is_public=is_public,
            is_collaborative=is_collaborative,
            playlist_description=None
        )

        assert_valid_schema(response, 'playlist_object_schema.yml')

        assert (
            response["name"] == "name"
        ), f"Response 'name' is: {response['name']}, should be: 'name'."
        assert (
            response["public"] == is_public
        ), f"Response 'public' is: {response['public']}, should be: '{is_public}'."
        assert (
            response["collaborative"] == is_collaborative
        ), f"Response 'collaborative' is: {response['collaborative']}, should be: '{is_collaborative}'."
        assert (
            response["description"] == None
        ), f"Response 'description' is: {response['description']}, should be: 'desc'."

        assert_current_user_owns_playlist(1)

        owned_playlist = self.get_owned_playlists_of_current_user()[0]

        assert_compare_playlists(
            owned_playlist, response, ["description", "followers", "snapshot_id", "tracks"]
        )

    @pytest.mark.parametrize(
        "is_public, is_collaborative",
        [
            (True, True),
            (None, True)
        ]
    )
    def test_create_playlist_colliding_properties(self, remove_owned_playlists, is_public, is_collaborative):
        response = self.post_create_playlist(
            status_code=400,
            token=OAUTH_TOKEN,
            user_id=USER_ID,
            playlist_name="name",
            is_public=is_public,
            is_collaborative=is_collaborative,
            playlist_description=None
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == _ERROR_COLLABORATIVE
        ), f"Actual error message: {response['error']['message']}, expected: {_ERROR_COLLABORATIVE}"

        assert_current_user_owns_playlist(0)
