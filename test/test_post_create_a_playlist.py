import pytest
import requests
import spotipy

from .assertions import (
    assert_valid_schema,
    assert_current_user_owns_playlist,
    assert_compare_playlists
)
from .base import TestBase
from constants import USER_ID, OAUTH_TOKEN, REDIRECT_URI

_ERROR_INVALID_USERNAME = "Invalid username"
_ERROR_COLLABORATIVE = "Collaborative playlists can only be private."
_ERROR_INSUFFICIENT_SCOPE = "Insufficient client scope"


class TestCreatePlaylist(TestBase):

    def get_token(self, scope):
        if scope == "":
            scope = 'playlist-read-collaborative'
        else:
            scope += ' playlist-read-collaborative'

        sp = spotipy.SpotifyOAuth(redirect_uri=REDIRECT_URI, scope=scope)
        return sp.get_access_token(check_cache=False)["access_token"]

    @pytest.fixture()
    def remove_owned_playlists(self):
        print("****SETUP****")
        yield 0
        print("****TEARDOWN****")
        owned_playlists = self.get_owned_playlists_of_current_user(OAUTH_TOKEN)
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

        assert_current_user_owns_playlist(0, OAUTH_TOKEN)

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

        assert_current_user_owns_playlist(1, OAUTH_TOKEN)

        owned_playlist = self.get_owned_playlists_of_current_user(OAUTH_TOKEN)[
            0]

        assert (
            owned_playlist["id"] == response["id"]
        ), f"User owns playlist with id: {owned_playlist['id']}, instead: {response['id']}."
        assert (
            owned_playlist["name"] == response["name"]
        ), f"User owns playlist with name: {owned_playlist['name']}, instead: {response['name']}"

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
            playlist_description="desc"
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
            response["description"] == "desc"
        ), f"Response 'description' is: {response['description']}, should be: 'desc'."

        assert_current_user_owns_playlist(1, OAUTH_TOKEN)

        owned_playlist = self.get_owned_playlists_of_current_user(OAUTH_TOKEN)[
            0]

        assert_compare_playlists(owned_playlist, response, [
                                 "followers", "snapshot_id", "tracks"])

    def test_TC17_create_playlist(self, remove_owned_playlists):
        response = self.post_create_playlist(
            status_code=400,
            token=OAUTH_TOKEN,
            user_id=USER_ID,
            playlist_name="name",
            is_public=True,
            is_collaborative=True,
            playlist_description="desc"
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == _ERROR_COLLABORATIVE
        ), f"Actual error message: {response['error']['message']}, expected: {_ERROR_COLLABORATIVE}"

        assert_current_user_owns_playlist(0, OAUTH_TOKEN)

    @pytest.mark.parametrize(
        "scope",
        [
            ("playlist-modify-private")
        ]
    )
    def test_TC21_create_playlist(self, remove_owned_playlists, scope):
        token = self.get_token(scope)

        response = self.post_create_playlist(
            token=token,
            user_id=USER_ID,
            playlist_name="name",
            is_public=False
        )

        assert_valid_schema(response, 'playlist_object_schema.yml')

        assert (
            response["name"] == "name"
        ), f"Response 'name' is: {response['name']}, should be: 'name'."
        assert (
            response["public"] == False
        ), f"Response 'public' is: {response['public']}, should be: 'True'."
        assert (
            response["collaborative"] == False
        ), f"Response 'collaborative' is: {response['collaborative']}, should be: 'False'."
        assert (
            response["description"] == None
        ), f"Response 'description' is: {response['description']}, should be: None."

        assert_current_user_owns_playlist(1, OAUTH_TOKEN)

        owned_playlist = self.get_owned_playlists_of_current_user(OAUTH_TOKEN)[
            0]
        assert_compare_playlists(
            owned_playlist, response, ["description",
                                       "followers", "snapshot_id", "tracks"]
        )

    @pytest.mark.parametrize(
        "scope",
        [
            ("playlist-modify-public")
        ]
    )
    def test_TC22_create_playlist(self, remove_owned_playlists, scope):
        token = self.get_token(scope)

        response = self.post_create_playlist(
            status_code=403,
            token=token,
            user_id=USER_ID,
            playlist_name="name",
            is_public=False
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == _ERROR_INSUFFICIENT_SCOPE
        ), f"Actual error message: {response['error']['message']}, expected: {_ERROR_INSUFFICIENT_SCOPE}"

        assert_current_user_owns_playlist(0, token)

    @pytest.mark.parametrize(
        "scope",
        [
            ("playlist-modify-private"),    # it fails
            ("playlist-modify-public"),
            ("")
        ]
    )
    def test_TC24_create_playlist(self, remove_owned_playlists, scope):
        token = self.get_token(scope)

        response = self.post_create_playlist(
            status_code=403,
            token=token,
            user_id=USER_ID,
            playlist_name="name",
            is_public=False,
            is_collaborative=True
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == _ERROR_INSUFFICIENT_SCOPE
        ), f"Actual error message: {response['error']['message']}, expected: {_ERROR_INSUFFICIENT_SCOPE}"

        assert_current_user_owns_playlist(0, token)
