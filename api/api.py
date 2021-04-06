import requests

from constants import API_URL, USER_ID, HEADERS


def get_album_by_id(album_id):
    url = f'{API_URL}/albums/{album_id}'

    return requests.get(url, headers=HEADERS)


def get_playlist_by_id(playlist_id):
    url = f'{API_URL}/playlists/{playlist_id}'

    return requests.get(url, headers=HEADERS)


def create_playlist(playlist_name, playlist_desc, is_playlist_public):
    url = f'{API_URL}/users/{USER_ID}/playlists'

    payload = {}

    if playlist_name is not None:
        payload["name"] = playlist_name
    if playlist_desc is not None:
        payload["description"] = playlist_desc
    if is_playlist_public is not None:
        payload["public"] = is_playlist_public

    return requests.post(url, headers=HEADERS, json=payload)


def add_items_to_playlist(playlist_id, track_uris):
    url = f'{API_URL}/playlists/{playlist_id}/tracks'

    query = "?uris=" + ",".join(track_uris)
    #query = f"?uris={','.join(track_uris)}"

    url += query

    return requests.post(url, headers=HEADERS)


def update_playlist_details(playlist_id, new_playlist_name, new_playlist_desc, is_new_playlist_public):
    url = f'{API_URL}/playlists/{playlist_id}'

    payload = {}

    if new_playlist_name is not None:
        payload["name"] = new_playlist_name
    if new_playlist_desc is not None:
        payload["description"] = new_playlist_desc
    if is_new_playlist_public is not None:
        payload["public"] = is_new_playlist_public

    return requests.put(url, headers=HEADERS, json=payload)


def delete_unfollow_a_playlist(playlist_id):
    url = f'{API_URL}/playlists/{playlist_id}/followers'

    return requests.delete(url, headers=HEADERS)


def get_current_user_profile():
    url = f"{API_URL}/me"

    return requests.get(url, headers=HEADERS)
