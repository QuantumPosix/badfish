from asynctest import patch
from tests.config import (
    INIT_RESP,
    FIRMWARE_INVENTORY_RESP,
    FIRMWARE_INVENTORY_1_RESP,
    FIRMWARE_INVENTORY_2_RESP,
    FIRMWARE_INVENTORY_RESP_CONTAINING_ERROR,
    RESPONSE_FIRMWARE_INVENTORY,
    RESPONSE_FIRMWARE_INVENTORY_NOT_ABLE_TO_ACCESS,
    RESPONSE_FIRMWARE_INVENTORY_NONE_RESPONSE,
)
from tests.test_base import TestBase, MockResponse


class TestFirmwareInventory(TestBase):
    option_arg = "--firmware-inventory"

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_firmware_inventory(self, mock_get, mock_post, mock_delete):
        responses_add = [
            FIRMWARE_INVENTORY_RESP,
            FIRMWARE_INVENTORY_1_RESP,
            FIRMWARE_INVENTORY_2_RESP,
        ]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_FIRMWARE_INVENTORY

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_firmware_inventory_json_invalid(self, mock_get, mock_post, mock_delete):
        responses_add = [""]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_FIRMWARE_INVENTORY_NOT_ABLE_TO_ACCESS

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_firmware_inventory_json_contains_error(
        self, mock_get, mock_post, mock_delete
    ):
        responses_add = [FIRMWARE_INVENTORY_RESP_CONTAINING_ERROR]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_FIRMWARE_INVENTORY_NOT_ABLE_TO_ACCESS

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("src.badfish.main.Badfish.get_request")
    def test_firmware_inventory_none_response(
        self, mock_get_req_call, mock_post, mock_delete
    ):
        responses_add = [FIRMWARE_INVENTORY_RESP, FIRMWARE_INVENTORY_1_RESP]
        responses = INIT_RESP + responses_add
        mock_get_req_call.side_effect = [
            MockResponse(responses[0], 200),
            MockResponse(responses[0], 200),
            MockResponse(responses[1], 200),
            MockResponse(responses[2], 200),
            MockResponse(responses[3], 200),
            MockResponse(responses[4], 200),
            MockResponse(responses[5], 200),
            None,
            MockResponse(responses[6], 200),
        ]
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_FIRMWARE_INVENTORY_NONE_RESPONSE
