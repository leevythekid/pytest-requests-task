from api.api import *


class TestBase:
    def get_album_by_id(self, album_id):
        response = get_album_by_id(album_id)

        return response

    def get_playlist_by_id(self, playlist_id=None):
        response = get_playlist_by_id(playlist_id)

        return response

    def post_create_playlist(self, playlist_name=None, playlist_desc=None, playlist_is_public=None):
        response = create_playlist(
            playlist_name=playlist_name,
            playlist_desc=playlist_desc,
            playlist_is_public=playlist_is_public
        )

        return response

    def post_add_items_to_playlist(self, playlist_id=None, track_uris=None):
        response = add_items_to_playlist(
            playlist_id=playlist_id,
            track_uris=track_uris
        )

        return response

    def put_update_playlist_details(self, playlist_id=None, new_playlist_name=None, new_playlist_desc=None, new_playlist_is_public=None):
        response = update_playlist_details(
            playlist_id=playlist_id,
            new_playlist_name=new_playlist_name,
            new_playlist_desc=new_playlist_desc,
            new_playlist_is_public=new_playlist_is_public
        )

        return response

    def delete_unfollow_a_playlist(self, playlist_id=None):
        response = delete_unfollow_a_playlist(
            playlist_id=playlist_id
        )

        return response
