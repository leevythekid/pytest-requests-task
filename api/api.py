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


def create_playlist(token, user_id, playlist_name, is_public, is_collaborative, playlist_description):
    if user_id == None:
        user_id = ""

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


"""
def get_album_by_id(album_id):
    url = f"{API_URL}/albums/{album_id}"

    return requests.get(url, headers=HEADERS)
"""


def get_playlist_items(playlist_id):
    url = f"{API_URL}/playlists/{playlist_id}/tracks"
    # ?market=HU&fields=items(track(uri))
    query = {"market": "HU", "fields": "items(track(uri))"}

    return requests.get(url, params=query, headers=HEADERS)


def get_playlist_by_id(playlist_id, bearer_token):
    url = f"{API_URL}/playlists/{playlist_id}"
    headers = {}

    if bearer_token is not None:
        headers["Authorization"] = f"Bearer {bearer_token}"

    return requests.get(url, headers=headers)


def get_list_of_current_users_playlists():
    url = f"{API_URL}/me/playlists"

    return requests.get(url, headers=HEADERS)


def add_items_to_playlist(playlist_id, track_uris):
    url = f"{API_URL}/playlists/{playlist_id}/tracks"
    query = {"uris": ",".join(track_uris)}

    return requests.post(url, params=query, headers=HEADERS)


def update_playlist_details(playlist_id, new_playlist_name, new_playlist_desc, is_new_playlist_public):
    url = f"{API_URL}/playlists/{playlist_id}"

    payload = {}

    if new_playlist_name is not None:
        payload["name"] = new_playlist_name
    if new_playlist_desc is not None:
        payload["description"] = new_playlist_desc
    if is_new_playlist_public is not None:
        payload["public"] = is_new_playlist_public

    return requests.put(url, headers=HEADERS, json=payload)


def unfollow_a_playlist(playlist_id):
    url = f"{API_URL}/playlists/{playlist_id}/followers"

    return requests.delete(url, headers=HEADERS)


def delete_items_from_playlist(playlist_id, tracks):
    url = f"{API_URL}/playlists/{playlist_id}/tracks"

    payload = {}

    if tracks is not None:
        payload["tracks"] = []
        for track in tracks:
            payload["tracks"].append(track)

    return requests.delete(url, headers=HEADERS, json=payload)


def get_current_user_profile():
    url = f"{API_URL}/me"

    return requests.get(url, headers=HEADERS)
