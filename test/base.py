import yaml
from jsonschema import validate
from api.api import get_album_by_id, get_playlist_by_id, create_playlist, add_items_to_playlist, update_playlist_details, delete_unfollow_a_playlist, get_current_user_profile, delete_items_from_playlist, auth_get_playlist_by_id, get_playlist_items


class TestBase:
    def get_album_by_id(self, album_id=None):
        response = get_album_by_id(album_id)

        return response

    def get_playlist_items(self, playlist_id):
        response = get_playlist_items(
            playlist_id=playlist_id
        )

        return response

    def auth_get_playlist_by_id(self, playlist_id, bearer_token=None):
        response = auth_get_playlist_by_id(
            playlist_id=playlist_id,
            bearer_token=bearer_token
        )

        return response

    def get_playlist_by_id(self, playlist_id=None):
        response = get_playlist_by_id(playlist_id)

        return response

    def post_create_playlist(self, playlist_name=None, playlist_desc=None, is_playlist_public=None):
        response = create_playlist(
            playlist_name=playlist_name,
            playlist_desc=playlist_desc,
            is_playlist_public=is_playlist_public
        )

        return response

    def post_add_items_to_playlist(self, playlist_id=None, track_uris=None):
        response = add_items_to_playlist(
            playlist_id=playlist_id,
            track_uris=track_uris
        )

        return response

    def put_update_playlist_details(self, playlist_id=None, new_playlist_name=None, new_playlist_desc=None, is_new_playlist_public=None):
        response = update_playlist_details(
            playlist_id=playlist_id,
            new_playlist_name=new_playlist_name,
            new_playlist_desc=new_playlist_desc,
            is_new_playlist_public=is_new_playlist_public
        )

        return response

    def delete_unfollow_a_playlist(self, playlist_id=None):
        response = delete_unfollow_a_playlist(
            playlist_id=playlist_id
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

    # Schema validation
    def assert_valid_schema(self, data, schema_file):
        """ Checks whether the given data matches the schema """
        with open(f'test/support/schemas/{schema_file}') as schema_file:
            schema = yaml.safe_load(schema_file.read())

        return validate(data, schema)

    # Fails if the playlist contains any of the given tracks
    def assert_playlist_contains_tracks(self, playlist_id, tracks):
        response = get_playlist_items(playlist_id)
        uris = []

        for item in response.json()['items']:
            uris.append(item['track']['uri'])

        for track in tracks:
            assert (
                track['uri'] not in uris), f'Track with URI: {track["uri"]} found in the playlist after deletion!'
