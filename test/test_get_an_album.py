import pytest
import random

from .assertions import assert_valid_schema, assert_album_contains_restrictions
from .base import TestBase
from constants import ALBUMS, OAUTH_TOKEN, EXPIRED_TOKEN, ALBUM_SUNRISE

_ALBUM = random.choice(ALBUMS)
_ERROR_NON_EXISTING_ID = "non existing id"
_ERROR_INVALID_ID = "invalid id"
_ERROR_NO_TOKEN = "No token provided"
_ERROR_BEARER = "Only valid bearer authentication supported"
_ERROR_INVALID_TOKEN = "Invalid access token"
_ERROR_EXPIRED_TOKEN = "The access token expired"
_ERROR_INVALID_MARKET = "Invalid market code"


class TestGetAnAlbum(TestBase):
    def test_TC1_get_album_by_id_with_market(self):
        response = self.get_album_by_id(
            token=OAUTH_TOKEN,
            album_id=_ALBUM["album_id"],
            market=_ALBUM["market"]
        )

        assert (
            response["id"] == _ALBUM["album_id"]
        ), f"Expected album_id: {_ALBUM['album_id']}, actual: {response['id']}"

        assert (
            "available_markets" not in response
        ), f"Response should not contain 'available_markets' property."

    def test_TC2_get_album_by_id_without_market(self):
        response = self.get_album_by_id(
            token=OAUTH_TOKEN,
            album_id=_ALBUM["album_id"]
        )

        assert (
            response["id"] == _ALBUM["album_id"]
        ), f"Expected album_id: {_ALBUM['album_id']}, actual: {response['id']}"

        assert (
            "available_markets" in response
        ), f"Response should contain 'available_markets' property."

    @pytest.mark.parametrize(
        "TC_ID, token, album_id, market, status_code, error_message",
        [
            ("TC-3", OAUTH_TOKEN, None, _ALBUM["market"], 400, _ERROR_INVALID_ID),
            ("TC-4", OAUTH_TOKEN, None, None, 400, _ERROR_INVALID_ID),
            ("TC-5", None, _ALBUM["album_id"], _ALBUM["market"], 401, _ERROR_NO_TOKEN),
            ("TC-6", None, _ALBUM["album_id"], None, 401, _ERROR_NO_TOKEN),
            ("TC-7", None, None, _ALBUM["market"], 401, _ERROR_NO_TOKEN),
            ("TC-8", None, None, None, 401, _ERROR_NO_TOKEN)
        ]
    )
    def test_missing_parameters(self, TC_ID, token, album_id,
                                market, status_code, error_message):
        response = self.get_album_by_id(
            TC_ID=TC_ID,
            status_code=status_code,
            token=token,
            album_id=album_id,
            market=market
        )

        assert_valid_schema(response, 'error_object_schema.yml', TC_ID)

        assert (
            response["error"]["message"] == error_message
        ), f"ERROR at TC-{TC_ID}. Response message is: {response['error']['message']}, should be: '{error_message}'."

    @pytest.mark.parametrize(
        "TC_ID, token, status_code, error_message",
        [
            ("TC-9#1", "", 400, _ERROR_BEARER),
            ("TC-9#2", "randonString123", 401, _ERROR_INVALID_TOKEN),
            ("TC-9#3", EXPIRED_TOKEN, 401, _ERROR_EXPIRED_TOKEN)
        ]
    )
    def test_TC9_invalid_token(self, TC_ID, token, status_code, error_message):
        response = self.get_album_by_id(
            TC_ID=TC_ID,
            status_code=status_code,
            token=token,
            album_id=_ALBUM["album_id"]
        )

        assert_valid_schema(response, 'error_object_schema.yml', TC_ID)

        assert (
            response["error"]["message"] == error_message
        ), f"ERROR at {TC_ID}. Response message is: {response['error']['message']}, should be: '{error_message}'."
        
    @pytest.mark.parametrize(
        "TC_ID, album_id",
        [
            ("TC-10#1", "16tDx6tKDmxMfNQyhfsaI"),
            ("TC-10#2", "16tDx6tKDmxMfNQyhfsaIgg"),
            ("TC-10#3", 1612),
            ("TC-10#4", False),
            ("TC-10#5", ["list"]),
            ("TC-10#6", {"id": "123"}),
            ("TC-10#7", {"id", "name"}),
        ]
    )
    def test_TC10_invalid_album_id_format(self, TC_ID, album_id):
        response = self.get_album_by_id(
            TC_ID=TC_ID,
            status_code=400,
            token=OAUTH_TOKEN,
            album_id=album_id
        )

        assert_valid_schema(response, 'error_object_schema.yml', TC_ID)

        assert (
            response["error"]["message"] == _ERROR_INVALID_ID
        ), f"Error at {TC_ID}. Response message is: {response['error']['message']}, should be: '{_ERROR_INVALID_ID}'."

    @pytest.mark.parametrize(
        "TC_ID, album_id",
        [
            ("TC-11#1", _ALBUM["album_id"].lower()),
            ("TC-11#2", _ALBUM["album_id"].upper()),
            ("TC-11#3", "s6pisHnukCHmnfot1v2jP2")
        ]
    )
    def test_TC11_invalid_album_id_content(self, TC_ID, album_id):
        response = self.get_album_by_id(
            status_code=404,
            token=OAUTH_TOKEN,
            album_id=album_id
        )

        assert_valid_schema(response, 'error_object_schema.yml', TC_ID)

        assert (
            response["error"]["message"] == _ERROR_NON_EXISTING_ID
        ), f"Response message is: {response['error']['message']}, should be: '{_ERROR_NON_EXISTING_ID}'."


    @pytest.mark.parametrize(
        "TC_ID, market",
        [
            ("TC-12#1", "Q"),
            ("TC-12#2", "QQ"),
            ("TC-12#3", "QQQ")
        ]
    )
    def test_TC12_invalid_market(self, TC_ID, market):
        response = self.get_album_by_id(
            TC_ID=TC_ID,
            status_code=400,
            token=OAUTH_TOKEN,
            album_id=_ALBUM["album_id"],
            market=market
        )

        assert_valid_schema(response, 'error_object_schema.yml', TC_ID)

        assert (
            response["error"]["message"] == _ERROR_INVALID_MARKET
        ), f"Error at {TC_ID}. Response message is: {response['error']['message']}, should be: '{_ERROR_INVALID_MARKET}'."

    def test_TC13_get_album_unavailable_in_market(self):
        response = self.get_album_by_id(
            token=OAUTH_TOKEN,
            album_id=ALBUM_SUNRISE["album_id"],
            market=ALBUM_SUNRISE["not_available_market"]
        )

        assert (
            response['id'] == ALBUM_SUNRISE['album_id']
        ), f"Expected album_id: {ALBUM_SUNRISE['album_id']}, actual: {response['id']}"

        assert_album_contains_restrictions(response)
