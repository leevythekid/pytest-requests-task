import pytest

from .base import TestBase
from constants import ALBUM_ID_AKPH_AKKEZDET, ALBUM_ID_BELGA_CSUMPA


class TestGetMethod(TestBase):
    @pytest.mark.parametrize("album_id, expected_status_code",
                             [(ALBUM_ID_AKPH_AKKEZDET, 200),
                              (ALBUM_ID_BELGA_CSUMPA, 200),
                              ("somerandom23213213", 400)])
    def test_get_album_by_id_status_code(self, album_id, expected_status_code):
        response = self.get_album_by_id(album_id=album_id)

        assert (response.status_code ==
                expected_status_code), f"Status code is expected to be {expected_status_code}"
#

    @pytest.mark.parametrize("album_id, expected_label",
                             [(ALBUM_ID_AKPH_AKKEZDET, "Akph"),
                              (ALBUM_ID_BELGA_CSUMPA, "Bëlga")])
    def test_get_album_by_id_label(self, album_id, expected_label):
        response = self.get_album_by_id(album_id=album_id)

        assert (response.json()[
                "label"] == expected_label), f"Label is expected to be {expected_label}"

    @pytest.mark.parametrize("album_id, expected_name",
                             [(ALBUM_ID_AKPH_AKKEZDET, "Akkezdet"),
                              (ALBUM_ID_BELGA_CSUMPA, "Csumpa")])
    def test_get_album_by_id_name(self, album_id, expected_name):
        response = self.get_album_by_id(album_id=album_id)

        assert (response.json()[
                "name"] == expected_name), f"Name is expected to be {expected_name}"

    def test_get_current_user_profile_schema(self):
        response = self.get_current_user_profile()

        self.assert_valid_schema(response.json(), "get_user_info_schema.yml")
