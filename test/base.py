import requests

from api.api import (
    get_album_by_id,
    create_playlist,
    get_list_of_current_users_playlists,
    unfollow_a_playlist,
    get_playlist_by_id,
    add_items_to_playlist,
    update_playlist_details,
    get_current_user_profile,
    delete_items_from_playlist,
    get_playlist_items
)
from constants import USER_ID


class TestBase():
    def get_album_by_id(self, status_code=200,
                        token=None, album_id=None, market=None):
        if album_id is None:
            album_id = ""

        response = get_album_by_id(
            token=token,
            album_id=album_id,
            market=market
        )

        if status_code is not None:
            assert (
                response.status_code == status_code
            ), f"Expected status code {status_code}, actual: {response.status_code}"

        return response.json()

    def post_create_playlist(self, status_code=201,
                             token=None, user_id=None,
                             playlist_name=None, is_public=None,
                             is_collaborative=None, playlist_description=None):
        if user_id is None:
            user_id = ""

        response = create_playlist(
            token=token,
            user_id=user_id,
            playlist_name=playlist_name,
            is_public=is_public,
            is_collaborative=is_collaborative,
            playlist_description=playlist_description
        )

        if status_code is not None:
            assert(
                response.status_code == status_code
            ), f"Expected status code {status_code}, actual: {response.status_code}"

        return response.json()

    def get_list_of_current_users_playlists(self, status_code=200):
        response = get_list_of_current_users_playlists()

        if status_code is not None:
            assert(
                response.status_code == status_code
            ), f"Expected status code {status_code}, actual: {response.status_code}"

        return response.json()

    def get_owned_playlists_of_current_user(self):
        response = self.get_list_of_current_users_playlists()
        playlists = []

        if len(response["items"]) > 0:
            for playlist in response["items"]:
                if playlist["owner"]["id"] == USER_ID:
                    playlists.append(playlist)

        return playlists

    def unfollow_a_playlist(self, status_code=200, playlist_id=None):
        response = unfollow_a_playlist(
            playlist_id=playlist_id
        )

        if status_code is not None:
            assert(
                response.status_code == status_code
            ), f"Expected status code {status_code}, actual: {response.status_code}"

        return response

    ######################################################
    # Functions below not used on the refactored version #
    ######################################################

    def get_album_by_id_old(self, album_id=None):
        response = get_album_by_id(album_id)

        return response

    def get_playlist_items(self, playlist_id):
        response = get_playlist_items(
            playlist_id=playlist_id
        )

        return response

    def get_playlist_by_id(self, playlist_id=None, bearer_token=None):
        response = get_playlist_by_id(
            playlist_id=playlist_id,
            bearer_token=bearer_token
        )

        return response.json()

    def post_add_items_to_playlist(self, playlist_id=None, track_uris=None):
        response = add_items_to_playlist(
            playlist_id=playlist_id,
            track_uris=track_uris
        )

        return response

    def put_update_playlist_details(self, playlist_id=None,
                                    new_playlist_name=None,
                                    new_playlist_desc=None,
                                    is_new_playlist_public=None):
        response = update_playlist_details(
            playlist_id=playlist_id,
            new_playlist_name=new_playlist_name,
            new_playlist_desc=new_playlist_desc,
            is_new_playlist_public=is_new_playlist_public
        )

        return response

    def delete_items_from_playlist(self, playlist_id, tracks):
        response = delete_items_from_playlist(
            playlist_id=playlist_id,
            tracks=tracks
        )

        return response

    def get_current_user_profile(self):
        response = get_current_user_profile()

        return response
