from unittest.mock import patch

from tests.config import (INIT_RESP, MEMORY_A5_RESP, MEMORY_B2_RESP,
                          MEMORY_MEMBERS_RESP, MEMORY_SUMMARY_RESP,
                          MEMORY_SUMMARY_RESP_FAULTY, RESPONSE_LS_MEMORY,
                          RESPONSE_LS_MEMORY_DETAILS_NOT_FOUND,
                          RESPONSE_LS_MEMORY_DETAILS_VALUE_ERROR,
                          RESPONSE_LS_MEMORY_SUMMARY_PROC_DATA_ERROR,
                          RESPONSE_LS_MEMORY_SUMMARY_VALUE_ERROR)
from tests.test_base import TestBase


class TestLsMemory(TestBase):
    option_arg = "--ls-memory"

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_memory(self, mock_get, mock_post, mock_delete):
        responses_add = [
            MEMORY_SUMMARY_RESP,
            MEMORY_MEMBERS_RESP,
            MEMORY_A5_RESP,
            MEMORY_B2_RESP,
        ]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_MEMORY

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_memory_summary_value_error(self, mock_get, mock_post, mock_delete):
        responses_add = [""]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_MEMORY_SUMMARY_VALUE_ERROR

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_memory_summary_proc_data_error(self, mock_get, mock_post, mock_delete):
        responses_add = [
            MEMORY_SUMMARY_RESP_FAULTY,
        ]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_MEMORY_SUMMARY_PROC_DATA_ERROR

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_memory_details_not_found(self, mock_get, mock_post, mock_delete):
        responses_add = [
            MEMORY_SUMMARY_RESP,
            "Not Found",
        ]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, [200, 200, 200, 200, 200, 404], responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_MEMORY_DETAILS_NOT_FOUND

    @patch("aiohttp.ClientSession.delete")
    @patch("aiohttp.ClientSession.post")
    @patch("aiohttp.ClientSession.get")
    def test_ls_memory_details_value_error(self, mock_get, mock_post, mock_delete):
        responses_add = [
            MEMORY_SUMMARY_RESP,
            "",
        ]
        responses = INIT_RESP + responses_add
        self.set_mock_response(mock_get, 200, responses)
        self.set_mock_response(mock_post, 200, "OK")
        self.set_mock_response(mock_delete, 200, "OK")
        self.args = [self.option_arg]
        _, err = self.badfish_call()
        assert err == RESPONSE_LS_MEMORY_DETAILS_VALUE_ERROR
