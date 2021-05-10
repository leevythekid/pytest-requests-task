import requests

from constants import API_URL, HEADERS


def get_album_by_id(token, album_id, market):
    url = f"{API_URL}/albums/{album_id}"
    headers = {}
    params = {}

    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    if market is not None:
        params["market"] = market

    return requests.get(url, params=params, headers=headers)


def create_playlist(token, user_id, playlist_name, is_public,
                    is_collaborative, playlist_description):
    url = f"{API_URL}/users/{user_id}/playlists"
    headers = {}
    payload = {}

    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    if playlist_name is not None:
        payload["name"] = playlist_name
    if is_public is not None:
        payload["public"] = is_public
    if is_collaborative is not None:
        payload["collaborative"] = is_collaborative
    if playlist_description is not None:
        payload["description"] = playlist_description

    return requests.post(url, headers=headers, json=payload)


def get_list_of_current_users_playlists():
    url = f"{API_URL}/me/playlists"

    return requests.get(url, headers=HEADERS)


def unfollow_a_playlist(playlist_id):
    url = f"{API_URL}/playlists/{playlist_id}/followers"

    return requests.delete(url, headers=HEADERS)
