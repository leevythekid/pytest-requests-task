from constants import ALBUM_ID_AKPH_AKKEZDET, ALBUM_ID_BELGA_CSUMPA
from base import TestBase
import pytest


class TestGetMethod(TestBase):
    @pytest.mark.parametrize("album_id, expected_status_code",
                             [(ALBUM_ID_AKPH_AKKEZDET, 200),
                              (ALBUM_ID_BELGA_CSUMPA, 200),
                              ("somerandom23213213", 400)])
    def test_get_album_by_id_status_code(self, album_id, expected_status_code):
        response = self.get_album_by_id(album_id=album_id)

        assert (response.status_code ==
                expected_status_code), f"The response code should be {expected_status_code}"

    @pytest.mark.parametrize("album_id, expected_label, expected_name",
                             [(ALBUM_ID_AKPH_AKKEZDET, "Akph", "Akkezdet"),
                              (ALBUM_ID_BELGA_CSUMPA, "Bëlga", "Csumpa")])
    def test_get_album_by_id_properties(self, album_id, expected_label, expected_name):
        response = self.get_album_by_id(album_id=album_id)

        assert (response.json()[
                "label"] == expected_label), f"The album with ID: '{album_id}' should have '{expected_label}' label"
        assert (response.json()[
                "name"] == expected_name), f"The album with ID: '{album_id}' should have '{expected_name}' name"
