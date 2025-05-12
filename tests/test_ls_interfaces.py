from unittest.mock import patch

from tests.config import (DEVICE_NIC_I, DEVICE_NIC_S, ETHERNET_INTERFACES_RESP,
                          ETHERNET_INTERFACES_RESP_NIC_INT,
                          ETHERNET_INTERFACES_RESP_NIC_SLOT, INIT_RESP,
                          NETWORK_ADAPTERS_RESP, NETWORK_DEV_FUNC_DET_RESP,
                          NETWORK_DEV_FUNC_RESP, NETWORK_PORTS_RESP,
                          NETWORK_PORTS_ROOT_RESP, RESPONSE_LS_ETHERNET,
                          RESPONSE_LS_INTERFACES,
                          RESPONSE_LS_INTERFACES_NOT_SUPPORTED,
                          RESPONSE_LS_INTERFACES_VALUE_ERROR)
from tests.test_base import TestBase


class TestLsInterfaces(TestBase):
    option_arg = "--ls-interfaces"

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_interfaces_adapters(self, mock_get, mock_post, mock_delete):
        responses_add = [
            NETWORK_ADAPTERS_RESP,
            NETWORK_PORTS_ROOT_RESP % (DEVICE_NIC_I, DEVICE_NIC_I),
            NETWORK_DEV_FUNC_RESP % (DEVICE_NIC_I, DEVICE_NIC_I),
            NETWORK_PORTS_RESP % DEVICE_NIC_I,
            NETWORK_DEV_FUNC_DET_RESP,
            NETWORK_PORTS_ROOT_RESP % (DEVICE_NIC_S, DEVICE_NIC_S),
            NETWORK_DEV_FUNC_RESP % (DEVICE_NIC_S, DEVICE_NIC_S),
            NETWORK_PORTS_RESP % DEVICE_NIC_S,
            NETWORK_DEV_FUNC_DET_RESP,
        ]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_INTERFACES

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_interfaces_network_value_error(self, mock_get, mock_post, mock_delete):
        responses_add = [
            "",
        ]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_INTERFACES_VALUE_ERROR

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_interfaces_ethernet(self, mock_get, mock_post, mock_delete):
        responses_add = [
            ETHERNET_INTERFACES_RESP,
            ETHERNET_INTERFACES_RESP_NIC_SLOT,
            ETHERNET_INTERFACES_RESP_NIC_INT,
        ]
        responses = INIT_RESP + responses_add
        status_codes = [200, 200, 200, 200, 200, 404, 200, 200, 200]
        self.set_mock_response(mock_get, status_codes, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_ETHERNET

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_interfaces_ethernet_not_supported(
        self, mock_get, mock_post, mock_delete
    ):
        responses_add = [
            "Not Found",
        ]
        responses = INIT_RESP + responses_add
        status_codes = [200, 200, 200, 200, 200, 404, 200, 404]
        self.set_mock_response(mock_get, status_codes, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_INTERFACES_NOT_SUPPORTED

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_interfaces_ethernet_value_error(self, mock_get, mock_post, mock_delete):
        responses_add = [
            "",
        ]
        responses = INIT_RESP + responses_add
        status_codes = [200, 200, 200, 200, 200, 404, 200, 200]
        self.set_mock_response(mock_get, status_codes, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_INTERFACES_VALUE_ERROR

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_interfaces_none_supported(self, mock_get, mock_post, mock_delete):
        responses_add = [
            "Not Found",
            "Not Found",
        ]
        responses = INIT_RESP + responses_add
        status_codes = [200, 200, 200, 200, 200, 404, 404]
        self.set_mock_response(mock_get, status_codes, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_INTERFACES_NOT_SUPPORTED
