from constants import ALBUM_ID_AKPH_AKKEZDET, ALBUM_ID_BELGA_CSUMPA
from base import TestBase
import pytest


class TestGetMethod(TestBase):
    def test_get_album_by_id_status_code(self):
        response = self.get_album_by_id(album_id=ALBUM_ID_AKPH_AKKEZDET)

        assert response.status_code == 200

    def test_get_album_by_id_properties(self):
        response = self.get_album_by_id(album_id=ALBUM_ID_BELGA_CSUMPA)

        assert response.json()["label"] == "Bëlga"
        assert response.json()["name"] == "Csumpa"
