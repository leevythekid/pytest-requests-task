from base import TestBase
import pytest


class TestPost(TestBase):
    def test_create_playlist(self):
        response = self.create_playlist(
            playlist_name="WfH playlist",
            playlist_desc="This is a playlist for anyone who is working from home.",
            playlist_is_public=True
        )

        assert response.status_code == 201

    def test_add_items_to_playlist(self):
        response = self.add_items_to_playlist(
            playlist_id="7wrPNtx38vpQmdqAY0DT5x",
            track_uris=["spotify:track:2TpDaiYW03b0aq9UNTkddU",
                        "spotify:track:46u28tBxptcjWUBAJedHkf"]
        )

        assert response.status_code == 201

    def test_add_items_to_playlist_schema(self):
        response = self.add_items_to_playlist(
            playlist_id="7wrPNtx38vpQmdqAY0DT5x",
            track_uris=["spotify:track:2TpDaiYW03b0aq9UNTkddU",
                        "spotify:track:46u28tBxptcjWUBAJedHkf"]
        )
        # print(response)
        print(response.json())

        # assert_valid_schema(response_in_json, schema)
