import pytest

from .assertions import (
    assert_compare_playlists,
    assert_current_user_owns_playlist,
    assert_valid_schema
)
from .base import TestBase
from .base import get_owned_playlists_of_current_user
from constants import USER_ID, OAUTH_TOKEN

_ERROR_INVALID_USERNAME = "Invalid username"
_ERROR_COLLABORATIVE = "Collaborative playlists can only be private."
_ERROR_PARSING = "Error parsing JSON."
_ERROR_INVALID_TOKEN = "Invalid access token"
_ERROR_NO_TOKEN = "No token provided"

_INVALID_TOKEN = "x"
_INVALID_USER_ID = ["invalid"]
_INVALID_NAME = {"name": "playlist_name"}
_INVALID_VISIBILITY = "yes"
_INVALID_COLLABORATIVE = "no"
_INVALID_DESCRIPTION = ["description"]

_VALID_NAME = "playlist_name"
_VALID_VISIBILITY = True
_VALID_COLLABORATIVE = False
_VALID_DESCRIPTION = "playlist_desc"


class TestCreatePlaylist(TestBase):

    @pytest.fixture()
    def remove_owned_playlists(self):
        yield 0
        owned_playlists = get_owned_playlists_of_current_user()
        for playlist in owned_playlists:
            self.unfollow_a_playlist(playlist_id=playlist["id"])

    @pytest.mark.parametrize(
        "TC_ID, token, user_id, playlist_name, is_public, is_collaborative, \
        playlist_description, status_code, error_message",
        [
            ("TC-1", OAUTH_TOKEN, None, _VALID_NAME, None,
             None, _VALID_DESCRIPTION, 404, _ERROR_INVALID_USERNAME),
            ("TC-2", OAUTH_TOKEN, None, _VALID_NAME, True,
             True, _INVALID_DESCRIPTION, 404, _ERROR_INVALID_USERNAME),
            ("TC-3", OAUTH_TOKEN, _INVALID_USER_ID, None, None,
             _VALID_COLLABORATIVE, None, 404, _ERROR_INVALID_USERNAME),
            ("TC-4", OAUTH_TOKEN, _INVALID_USER_ID, _INVALID_NAME, None,
             True, None, 404, _ERROR_INVALID_USERNAME)
        ]
    )
    def test_invalid_user_id(self, TC_ID, remove_owned_playlists,
                             token, user_id, playlist_name,
                             is_public, is_collaborative,
                             playlist_description,
                             status_code, error_message):
        response = self.post_create_playlist(
            TC_ID=TC_ID,
            status_code=status_code,
            token=token,
            user_id=user_id,
            playlist_name=playlist_name,
            is_public=is_public,
            is_collaborative=is_collaborative,
            playlist_description=playlist_description,
        )

        assert_valid_schema(response, "error_object_schema.yml", TC_ID)

        assert (
            response["error"]["message"] == error_message
        ), f"ERROR at {TC_ID}. Response message is: {response['error']['message']}, should be: '{error_message}'."

        assert_current_user_owns_playlist(0, TC_ID)

    @pytest.mark.parametrize(
        "TC_ID, token, user_id, playlist_name, is_public, is_collaborative, \
        playlist_description, status_code, error_message",
        [
            ("TC-5", OAUTH_TOKEN, USER_ID, None, _INVALID_VISIBILITY,
             None, _INVALID_DESCRIPTION, 400, _ERROR_PARSING),
            ("TC-6", _INVALID_TOKEN, None, _INVALID_NAME,
             None, None, None, 401, _ERROR_INVALID_TOKEN),
            ("TC-7", _INVALID_TOKEN, _INVALID_USER_ID, _INVALID_NAME, _INVALID_VISIBILITY,
             _INVALID_COLLABORATIVE, _INVALID_DESCRIPTION, 401, _ERROR_INVALID_TOKEN),
            ("TC-8", _INVALID_TOKEN, _INVALID_USER_ID, _VALID_NAME, _VALID_VISIBILITY,
             _INVALID_COLLABORATIVE, _VALID_DESCRIPTION, 401, _ERROR_INVALID_TOKEN),
            ("TC-9", _INVALID_TOKEN, USER_ID, None, None, _VALID_COLLABORATIVE,
             _VALID_DESCRIPTION, 401, _ERROR_INVALID_TOKEN),
            ("TC-10", None, None, None, None, _INVALID_COLLABORATIVE,
             _INVALID_DESCRIPTION, 401, _ERROR_NO_TOKEN),
            ("TC-11", None, None, _INVALID_NAME, _INVALID_VISIBILITY,
             _VALID_COLLABORATIVE, _VALID_DESCRIPTION, 401, _ERROR_NO_TOKEN),
            ("TC-12", None, _INVALID_USER_ID, None, _VALID_VISIBILITY,
             None, _INVALID_DESCRIPTION, 401, _ERROR_NO_TOKEN),
            ("TC-13", None, USER_ID, _INVALID_NAME, _VALID_VISIBILITY,
             _INVALID_COLLABORATIVE, None, 401, _ERROR_NO_TOKEN),
            ("TC-14", None, USER_ID, _VALID_NAME, _INVALID_VISIBILITY,
             _VALID_COLLABORATIVE, None, 401, _ERROR_NO_TOKEN)
        ]
    )
    def test_invalid_properties(self, TC_ID, remove_owned_playlists,
                                token, user_id, playlist_name,
                                is_public, is_collaborative,
                                playlist_description,
                                status_code, error_message):
        response = self.post_create_playlist(
            TC_ID=TC_ID,
            status_code=status_code,
            token=token,
            user_id=user_id,
            playlist_name=playlist_name,
            is_public=is_public,
            is_collaborative=is_collaborative,
            playlist_description=playlist_description,
        )

        assert_valid_schema(response, "error_object_schema.yml", TC_ID)

        assert (
            response["error"]["message"] == error_message
        ), f"ERROR at {TC_ID}. Response message is: {response['error']['message']}, should be: '{error_message}'."

        assert_current_user_owns_playlist(0, TC_ID)

    def test_TC15_create_playlist_with_required_fields(self, remove_owned_playlists):
        response = self.post_create_playlist(
            token=OAUTH_TOKEN,
            user_id=USER_ID,
            playlist_name="name"
        )

        assert_valid_schema(response, "playlist_object_schema.yml", TC_ID)

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

        owned_playlist = get_owned_playlists_of_current_user()[0]

        assert_compare_playlists(
            owned_playlist, response, ["description",
                                       "followers", "snapshot_id", "tracks"]
        )

    @pytest.mark.parametrize(
        "TC_ID, is_public, is_collaborative",
        [
            ("TC-16#1", True, False),
            ("TC-16#2", False, True),
            ("TC-16#3", False, False)
        ]
    )
    def test_TC16_create_playlist_with_all_fields(
            self, TC_ID, remove_owned_playlists,
            is_public, is_collaborative
    ):

        response = self.post_create_playlist(
            TC_ID=TC_ID,
            token=OAUTH_TOKEN,
            user_id=USER_ID,
            playlist_name="name",
            is_public=is_public,
            is_collaborative=is_collaborative,
            playlist_description=None
        )

        assert_valid_schema(response, "playlist_object_schema.yml", TC_ID)

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

        assert_current_user_owns_playlist(1, TC_ID)

        owned_playlist = get_owned_playlists_of_current_user()[0]

        assert_compare_playlists(
            owned_playlist, response,
            ["description", "followers", "snapshot_id", "tracks"], TC_ID
        )

    @pytest.mark.parametrize(
        "TC_ID, is_public, is_collaborative",
        [
            ("TC-17", True, True),
            ("TC-20", None, True)
        ]
    )
    def test_create_playlist_colliding_properties(self, TC_ID, remove_owned_playlists,
                                                  is_public, is_collaborative):
        response = self.post_create_playlist(
            TC_ID=TC_ID,
            status_code=400,
            token=OAUTH_TOKEN,
            user_id=USER_ID,
            playlist_name="name",
            is_public=is_public,
            is_collaborative=is_collaborative,
            playlist_description=None
        )

        assert_valid_schema(response, "error_object_schema.yml", TC_ID)

        assert (
            response["error"]["message"] == _ERROR_COLLABORATIVE
        ), f"ERROR at {TC_ID}. Actual error message: {response['error']['message']}, expected: {_ERROR_COLLABORATIVE}"

        assert_current_user_owns_playlist(0, TC_ID)
