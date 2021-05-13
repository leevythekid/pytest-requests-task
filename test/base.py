import requests

from api.api import (
    get_album_by_id,
    create_playlist,
    get_list_of_current_users_playlists,
    unfollow_a_playlist
)
from constants import USER_ID


class TestBase():
    def get_album_by_id(self, TC_ID=None, status_code=200,
                        token=None, album_id=None, market=None):

        error_msg = create_error_message(TC_ID) 

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
            ), f"{error_msg}Expected status code {status_code}, actual: {response.status_code}"

        return response.json()

    def post_create_playlist(self, TC_ID=None, status_code=201,
                             token=None, user_id=None,
                             playlist_name=None, is_public=None,
                             is_collaborative=None, playlist_description=None):

        error_msg = create_error_message(TC_ID)
        
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
            ), f"{error_msg}Expected status code {status_code}, actual: {response.status_code}"

        return response.json()

    def unfollow_a_playlist(self, status_code=200, playlist_id=None):
        if playlist_id is None:
            playlist_id == ""

        response = unfollow_a_playlist(
            playlist_id=playlist_id
        )

        if status_code is not None:
            assert(
                response.status_code == status_code
            ), f"Expected status code {status_code}, actual: {response.status_code}"

        return response


def get_owned_playlists_of_current_user(status_code=200):
    response = get_list_of_current_users_playlists()

    if status_code is not None:
        assert(
            response.status_code == status_code
        ), f"Expected status code {status_code}, actual: {response.status_code}"
    
    response = response.json()
    playlists = []

    if len(response["items"]) > 0:
        for playlist in response["items"]:
            if playlist["owner"]["id"] == USER_ID:
                playlists.append(playlist)

    return playlists


def create_error_message(TC_ID):
    if TC_ID is not None:
        error_msg = f"Error at {TC_ID}. "
    else:
        error_msg = ""
    
    return error_msg


""" def get_list_of_current_users_playlists(status_code=200):
    response = get_list_of_current_users_playlists()

    if status_code is not None:
        assert(
            response.status_code == status_code
        ), f"Expected status code {status_code}, actual: {response.status_code}"

    return response.json() """