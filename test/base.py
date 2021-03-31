from api.api import get_album_by_id, create_playlist, add_items_to_playlist, update_playlist_details


class TestBase:
    def get_album_by_id(self, album_id):
        response = get_album_by_id(album_id)

        return response

    def create_playlist(self, playlist_name=None, playlist_desc=None, playlist_is_public=None):
        response = create_playlist(
            playlist_name=playlist_name,
            playlist_desc=playlist_desc,
            playlist_is_public=playlist_is_public
        )

        return response

    def add_items_to_playlist(self, playlist_id, track_uris):
        response = add_items_to_playlist(
            playlist_id=playlist_id,
            track_uris=track_uris
        )

        return response

    def update_playlist_details(self, playlist_id, new_playlist_name, new_playlist_desc, new_playlist_is_public):
        response = update_playlist_details(
            playlist_id=playlist_id,
            new_playlist_name=new_playlist_name,
            new_playlist_desc=new_playlist_desc,
            new_playlist_is_public=new_playlist_is_public
        )

        return response
