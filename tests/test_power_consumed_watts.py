from asynctest import patch
from tests.config import (
    INIT_RESP, NO_POWER, POWER_CONSUMED_RESP, RESPONSE_NO_POWER_CONSUMED, RESPONSE_POWER_CONSUMED_OK, RESPONSE_POWER_CONSUMED_404,
     RESPONSE_POWER_CONSUMED_VAL_ERR,

)
from tests.test_base import  TestBase

class TestPowerConsumed(TestBase):
    args = ["--get-power-consumed"]

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_power_consumed(self, mock_get, mock_post, mock_delete):
        responses = INIT_RESP + [POWER_CONSUMED_RESP]
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK", True)
        self.set_mock_response(mock_delete, 200, "OK")
        _, err = self.badfish_call()
        assert err == RESPONSE_POWER_CONSUMED_OK

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_power_consumed_404(self, mock_get, mock_post, mock_delete):
        responses = INIT_RESP + [POWER_CONSUMED_RESP]
        self.set_mock_response(mock_get, [200,200,200,200,200,404], responses)
        self.set_mock_response(mock_post, 200, "OK", True)
        self.set_mock_response(mock_delete, 200, "OK")
        _, err = self.badfish_call()
        assert err == RESPONSE_POWER_CONSUMED_404

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_no_power(self, mock_get, mock_post, mock_delete):
        responses = INIT_RESP + [NO_POWER]
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK", True)
        self.set_mock_response(mock_delete, 200, "OK")
        _, err = self.badfish_call()
        assert err == RESPONSE_NO_POWER_CONSUMED

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_power_consumed_value_error(self, mock_get, mock_post, mock_delete):
        responses_add = [""]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK", True)
        self.set_mock_response(mock_delete, 200, "OK")
        _, err = self.badfish_call()
        assert err == RESPONSE_POWER_CONSUMED_VAL_ERR
