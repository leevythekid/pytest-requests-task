from base import TestBase
import pytest


class TestPut(TestBase):
    def test_update_playlist_details(self):
        response = self.update_playlist_details(
            playlist_id="7wrPNtx38vpQmdqAY0DT5x",
            new_playlist_name="WfH updated name",
            new_playlist_desc="new description",
            new_playlist_is_public=True
        )

        assert response.status_code == 200
