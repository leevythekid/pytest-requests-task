import requests
from constants import API_URL, OAUTH_TOKEN, OAUTH_VALUE, USER_ID, HEADERS


def get_album_by_id(album_id):
    url = f'{API_URL}/albums/{album_id}'

    return requests.get(url, headers=HEADERS)


def get_playlist_by_id(playlist_id):
    url = f'{API_URL}/playlists/{playlist_id}'

    return requests.get(url, headers=HEADERS)


def create_playlist(playlist_name, playlist_desc, playlist_is_public):
    url = f'{API_URL}/users/{USER_ID}/playlists'

    payload = {}

    if playlist_name is not None:
        payload["name"] = playlist_name
    if playlist_desc is not None:
        payload["description"] = playlist_desc
    if playlist_is_public is not None:
        payload["public"] = playlist_is_public

    return requests.post(url, headers=HEADERS, json=payload)


def add_items_to_playlist(playlist_id, track_uris):
    url = f'{API_URL}/playlists/{playlist_id}/tracks'

    query = "?uris="

    if track_uris is not None:
        for index, uri in enumerate(track_uris):
            if index == len(track_uris) - 1:
                query += uri
            else:
                query += uri + ","

    url += query

    print("URL: " + url)

    return requests.post(url, headers=HEADERS)


def update_playlist_details(playlist_id, new_playlist_name, new_playlist_desc, new_playlist_is_public):
    url = f'{API_URL}/playlists/{playlist_id}'

    payload = {}

    if new_playlist_name is not None:
        payload["name"] = new_playlist_name
    if new_playlist_desc is not None:
        payload["description"] = new_playlist_desc
    if new_playlist_is_public is not None:
        payload["public"] = new_playlist_is_public

    return requests.put(url, headers=HEADERS, json=payload)


def delete_unfollow_a_playlist(playlist_id):
    url = f'{API_URL}/playlists/{playlist_id}/followers'

    return requests.delete(url, headers=HEADERS)
