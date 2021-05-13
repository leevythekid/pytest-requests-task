import yaml

from .base import get_owned_playlists_of_current_user, create_error_message
from jsonschema import validate

def assert_valid_schema(data, schema_file, TC_ID=None):
    # Schema validation - Checks whether the given data matches the schema
    error_msg = create_error_message(TC_ID)
    
    with open(f"test/support/schemas/{schema_file}") as schema_file:
        schema = yaml.safe_load(schema_file.read())

    try:
        validation_result = validate(data, schema)
    except Exception:
        validation_result = Exception
    
    assert (validation_result == None), f"{error_msg}An exception occured during validation."

def assert_album_contains_restrictions(response_album):
    # Checks if every item of the given album contains 'restrictions' property which contains value {"reason": "market"}
    for track in response_album["tracks"]["items"]:
        assert (
            "restrictions" in track
        ), f"Track with id: {track['id']} and name: {track['name']} does not contains the 'restrictions' property."
        assert (
            ("reason", "market") in track["restrictions"].items()
        ), f"Track's {track['id']} 'restriction' property contains: {track['restrictions']} insted of: {{\"reason\": \"market\"}} "

def assert_current_user_owns_playlist(number_of_playlists, TC_ID=None):
    # Checks if the current user owns exactly {number_of_playlists} playlist(s)
    error_msg = create_error_message(TC_ID)
    
    number_of_owned_playlists_of_current_user = len(get_owned_playlists_of_current_user())
    assert (
        number_of_owned_playlists_of_current_user == number_of_playlists
    ), f"{error_msg}Current playler owns {number_of_owned_playlists_of_current_user} playlist(s), insted of: {number_of_playlists}."


def assert_compare_playlists(owned_playlist, created_playlist, ignored_keys, TC_ID=None):
    # Compare two playlists ignoring the given properties

    error_msg = create_error_message(TC_ID)
    
    for key in ignored_keys:
        if key in owned_playlist.keys():
            owned_playlist.pop(key)
        if key in created_playlist.keys():
            created_playlist.pop(key)

    assert (
        owned_playlist == created_playlist
    ), f"{error_msg}The given playlists are different. owned_playlist: {owned_playlist}\ncreated_playlist:{created_playlist}"

