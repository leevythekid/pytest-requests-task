import pytest

from .base import TestBase
from constants import ALBUM_ID_AKPH_AKKEZDET


class TestAuthorizationMethod(TestBase):
    @pytest.fixture()
    def create_playlist(self):
        print("*****SETUP*****")
        response = self.post_create_playlist(
            playlist_name="Beforehook playlist",
            playlist_desc="beforehook playlist description",
            is_playlist_public=True
        )
        yield response
        print("*****TEARDOWN*****")
        self.delete_unfollow_a_playlist(response.json()["id"])

    @pytest.mark.parametrize("bearer_token, expected_status_code",
                             [("", 400),
                              ("SOMERANDOMStr123", 401),
                              ("BQDUw1iEySSR1Vdcqy1sP-dy21M2zy5GwVhAcEXz8EOO2WiKU4qKMhisd3T9ew0xHjxaSJVGypFRsoPQlrW27FHBynRgNYBCuHwyaouceYWQ-GRCvMOT5DW0XwefrH0ldLFQBV7QGJQ2josSItn_bxZMwKA9TWSj6ZauYWMqc7vgxpdFTshYyqJTpFkKtw0_gGFPDEoSlV-Xyq2vIuTt7kw5mOCOhT0U9i70MlFvTwVgIRC_ZBPF7RIaIHxABpsWCL5F1NjkiOLuk5dxl5w5yM3Arhx3Y9vY98uUgm7z", 401),
                              (None, 401)
                              ])
    def test_get_playlist_by_id_status_code(self, create_playlist, bearer_token, expected_status_code):
        response = self.auth_get_playlist_by_id(
            playlist_id=create_playlist.json()["id"],
            bearer_token=bearer_token
        )

        assert response.status_code == expected_status_code