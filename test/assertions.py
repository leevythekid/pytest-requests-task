import yaml

from .base import TestBase
from jsonschema import validate

# Schema validation - Checks whether the given data matches the schema
def assert_valid_schema(data, schema_file):
    with open(f"test/support/schemas/{schema_file}") as schema_file:
        schema = yaml.safe_load(schema_file.read())

    return validate(data, schema)

# Checks if the given album object contains 'restrictions' property with value {"reason": "market"}
def assert_album_contains_restrictions(response_album):
    for track in response_album["tracks"]["items"]:
        assert (
            "restrictions" in track
        ), f"Track with id: {track['id']} and name: {track['name']} does not contains the 'restrictions' property."
        assert (
            ("reason", "market") in track["restrictions"].items()
        ), f"Track's {track['id']} 'restriction' property contains: {track['restrictions']} insted of: {{\"reason\": \"market\"}} "

# Fails if the playlist contains any of the given tracks
def assert_playlist_contains_tracks(playlist_id, tracks):
    response = get_playlist_items(playlist_id)
    uris = []

    for item in response.json()["items"]:
        uris.append(item["track"]["uri"])

    for track in tracks:
        assert (
            track["uri"] not in uris
        ), f"Track with URI: {track['uri']} found in the playlist after deletion!"

# Checks if the current user owns exactly {number_of_playlists} playlist(s)
def assert_current_user_owns_playlist(number_of_playlists):
    assert (
        len(TestBase().get_owned_playlists_of_current_user()) == number_of_playlists
    ), f"Current playler owns {len(testbase.get_owned_playlists_of_current_user())} playlist(s), insted of: {number_of_playlists}."

# Compare two playlists ignoring the given properties
def assert_compare_playlists(owned_playlist, created_playlist, ignored_keys):
    for key in ignored_keys:
        if key in owned_playlist.keys():
            owned_playlist.pop(key)
        if key in created_playlist.keys():
            created_playlist.pop(key)

    assert (
        owned_playlist == created_playlist
    ), f"The given playlists are different. playlist1: {owned_playlist}\nplaylist2:{created_playlist}"

