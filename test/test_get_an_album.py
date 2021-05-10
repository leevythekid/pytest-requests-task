import pytest
import random

from .assertions import assert_valid_schema, assert_album_contains_restrictions
from .base import TestBase
from constants import ALBUM_ID_LIST, OAUTH_TOKEN, EXPIRED_TOKEN, ALBUM_SUNRISE

_ALBUM = random.choice(ALBUM_ID_LIST)
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
        "token, album_id, market, status_code, error_message",
        [
            (OAUTH_TOKEN, None, _ALBUM["market"], 400, _ERROR_INVALID_ID),
            (OAUTH_TOKEN, None, None, 400, _ERROR_INVALID_ID),
            (None, _ALBUM["album_id"], _ALBUM["market"], 401, _ERROR_NO_TOKEN),
            (None, _ALBUM["album_id"], None, 401, _ERROR_NO_TOKEN),
            (None, None, _ALBUM["market"], 401, _ERROR_NO_TOKEN),
            (None, None, None, 401, _ERROR_NO_TOKEN)
        ]
    )
    def test_missing_parameters(self, token, album_id,
                                market, status_code, error_message):
        response = self.get_album_by_id(
            status_code=status_code,
            token=token,
            album_id=album_id,
            market=market
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == error_message
        ), f"Response message is: {response['error']['message']}, should be: '{error_message}'."

    @pytest.mark.parametrize(
        "token, status_code, error_message",
        [
            ("", 400, _ERROR_BEARER),
            ("randonString123", 401, _ERROR_INVALID_TOKEN),
            (EXPIRED_TOKEN, 401, _ERROR_EXPIRED_TOKEN)
        ]
    )
    def test_TC9_invalid_token(self, token, status_code, error_message):
        response = self.get_album_by_id(
            status_code=status_code,
            token=token,
            album_id=_ALBUM["album_id"]
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == error_message
        ), f"Response message is: {response['error']['message']}, should be: '{error_message}'."

    @pytest.mark.parametrize(
        "album_id",
        [
            ("16tDx6tKDmxMfNQyhfsaI"),
            ("16tDx6tKDmxMfNQyhfsaIgg"),
            (1612),
            (False),
            (["list"]),
            ({"id": "123"}),
            ({"id", "name"}),
        ]
    )
    def test_TC10_invalid_album_id_format(self, album_id):
        response = self.get_album_by_id(
            status_code=400,
            token=OAUTH_TOKEN,
            album_id=album_id
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == _ERROR_INVALID_ID
        ), f"Response message is: {response['error']['message']}, should be: '{_ERROR_INVALID_ID}'."

    @pytest.mark.parametrize(
        "album_id",
        [
            (_ALBUM["album_id"].lower()),
            (_ALBUM["album_id"].upper()),
            ("s6pishnukchmnfot1v2jp2")
        ]
    )
    def test_TC11_invalid_album_id_content(self, album_id):
        response = self.get_album_by_id(
            status_code=404,
            token=OAUTH_TOKEN,
            album_id=album_id
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == _ERROR_NON_EXISTING_ID
        ), f"Response message is: {response['error']['message']}, should be: '{_ERROR_NON_EXISTING_ID}'."


    @pytest.mark.parametrize(
        "market",
        [
            ("Q"),
            ("QQ"),
            ("QQQ")
        ]
    )
    def test_TC12_invalid_market(self, market):
        response = self.get_album_by_id(
            status_code=400,
            token=OAUTH_TOKEN,
            album_id=_ALBUM["album_id"],
            market=market
        )

        assert_valid_schema(response, 'error_object_schema.yml')

        assert (
            response["error"]["message"] == _ERROR_INVALID_MARKET
        ), f"Response message is: {response['error']['message']}, should be: '{_ERROR_INVALID_MARKET}'."

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