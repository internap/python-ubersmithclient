# Copyright 2016 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from hamcrest import assert_that, equal_to
from mock import patch, MagicMock

import ubersmith_client
from tests.ubersmith_json.response_data_structure import a_response_data


class UbersmithRequestGetTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://ubersmith.example.com/'
        self.username = 'admin'
        self.password = 'test'

        self.auth = (self.username, self.password)
        self.timeout = 60

    @patch('ubersmith_client.ubersmith_request_get.requests')
    def test_api_get_method_returns_without_arguments(self, requests_mock):
        json_data = {
            'company': 'council of ricks'
        }
        expected_call = self.expect_a_ubersmith_call(requests_mock=requests_mock,
                                                     method='client.list',
                                                     returning=a_response_data(data=json_data))

        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password, use_http_get=True)
        response = ubersmith_api.client.list()

        assert_that(response, equal_to(json_data))

        expected_call()

    @patch('ubersmith_client.ubersmith_request_get.requests')
    def test_api_get_method_returns_with_arguments(self, request_mock):
        json_data = {
            'group_id': '1',
            'client_id': '30001',
            'assignment_count': '1'
        }
        expected_call = self.expect_a_ubersmith_call(requests_mock=request_mock,
                                                     method='device.ip_group_list',
                                                     fac_id=1,
                                                     client_id=30001,
                                                     returning=a_response_data(data=json_data))

        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password, use_http_get=True)
        response = ubersmith_api.device.ip_group_list(fac_id=1, client_id=30001)

        assert_that(response, equal_to(json_data))

        expected_call()

    @patch('ubersmith_client.ubersmith_request_get.requests')
    def test_api_get_support_ticket_submit_allow_file_upload(self, request_mock):
        expected_files = {'attach[0]': ('filename.pdf', b'filecontent')}
        expected_call = self.expect_a_ubersmith_call_with_files(requests_mock=request_mock,
                                                                method='support.ticket_submit',
                                                                subject='that I used to know',
                                                                body='some body',
                                                                returning=a_response_data(data='42'),
                                                                files=expected_files)

        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password, use_http_get=True)

        response = ubersmith_api.support.ticket_submit(subject='that I used to know',
                                                       body='some body',
                                                       files=expected_files)

        assert_that(response, equal_to('42'))

        expected_call()

    def expect_a_ubersmith_call(self, requests_mock, returning=None, **kwargs):
        response = MagicMock(status_code=200, headers={'content-type': 'application/json'})
        requests_mock.get = MagicMock(return_value=response)
        response.json = MagicMock(return_value=returning)

        def assert_called_with():
            requests_mock.get.assert_called_with(auth=self.auth, params=kwargs, timeout=self.timeout, url=self.url,
                                                 headers={'user-agent': 'python-ubersmithclient'})
            response.json.assert_called_with()

        return assert_called_with

    def expect_a_ubersmith_call_with_files(self, requests_mock, returning=None, files=None, **kwargs):
        response = MagicMock(status_code=200, headers={'content-type': 'application/json'})
        requests_mock.get = MagicMock(return_value=response)
        response.json = MagicMock(return_value=returning)

        def assert_called_with():
            requests_mock.get.assert_called_with(auth=self.auth, params=kwargs, timeout=self.timeout, url=self.url,
                                                 files=files,
                                                 headers={'user-agent': 'python-ubersmithclient'})
            response.json.assert_called_with()

        return assert_called_with
