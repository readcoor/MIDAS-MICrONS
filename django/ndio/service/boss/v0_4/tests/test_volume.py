# Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ndio.service.boss.v0_4.volume import VolumeService_0_4
from ndio.ndresource.boss.resource import ChannelResource
import blosc
import numpy
from requests import HTTPError, PreparedRequest, Response, Session
import unittest
from unittest.mock import patch

class TestVolume_v0_4(unittest.TestCase):
    def setUp(self):
        self.vol = VolumeService_0_4()
        self.chan = ChannelResource('chan', 'foo', 'bar', datatype='uint16')

    @patch('requests.Session', autospec=True)
    def test_cutout_create_success(self, mock_session):
        resolution = 0
        x_range = '20:40'
        y_range = '50:70'
        z_range = '30:50'
        time_range = '10:25'
        data = numpy.random.randint(0, 3000, (15, 20, 20, 20), numpy.uint16)
        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'

        mock_session.prepare_request.return_value = PreparedRequest()
        fake_response = Response()
        fake_response.status_code = 201
        mock_session.send.return_value = fake_response
        send_opts = {}

        self.vol.cutout_create(
            self.chan, resolution, x_range, y_range, z_range, time_range, data,
            url_prefix, auth, mock_session, send_opts)

    @patch('requests.Session', autospec=True)
    def test_cutout_create_failure(self, mock_session):
        resolution = 0
        x_range = '20:40'
        y_range = '50:70'
        z_range = '30:50'
        time_range = '10:25'
        data = numpy.random.randint(0, 3000, (15, 20, 20, 20), numpy.uint16)
        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'

        mock_session.prepare_request.return_value = PreparedRequest()
        fake_response = Response()
        fake_response.status_code = 403
        mock_session.send.return_value = fake_response
        send_opts = {}

        with self.assertRaises(HTTPError):
            self.vol.cutout_create(
                self.chan, resolution, x_range, y_range, z_range, time_range, data,
                url_prefix, auth, mock_session, send_opts)

    @patch('requests.Session', autospec=True)
    def test_cutout_get_success(self, mock_session):
        resolution = 0
        x_range = '20:40'
        y_range = '50:70'
        z_range = '30:50'
        time_range = '10:25'
        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'

        fake_prepped_req = PreparedRequest()
        fake_prepped_req.headers = {}
        mock_session.prepare_request.return_value = fake_prepped_req 

        data = numpy.random.randint(0, 3000, (15, 20, 20, 20), numpy.uint16)
        compressed_data = blosc.pack_array(data)
        fake_response = Response()
        fake_response.status_code = 200
        fake_response._content = compressed_data
        mock_session.send.return_value = fake_response
        send_opts = {}

        actual = self.vol.cutout_get(
            self.chan, resolution, x_range, y_range, z_range, time_range,
            url_prefix, auth, mock_session, send_opts)

        numpy.testing.assert_array_equal(data, actual)

    @patch('requests.Session', autospec=True)
    def test_cutout_get_failure(self, mock_session):
        resolution = 0
        x_range = '20:40'
        y_range = '50:70'
        z_range = '30:50'
        time_range = '10:25'
        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'

        fake_prepped_req = PreparedRequest()
        fake_prepped_req.headers = {}
        mock_session.prepare_request.return_value = fake_prepped_req 
        fake_response = Response()
        fake_response.status_code = 403
        mock_session.send.return_value = fake_response
        send_opts = {}

        with self.assertRaises(HTTPError):
            actual = self.vol.cutout_get(
                self.chan, resolution, x_range, y_range, z_range, time_range,
                url_prefix, auth, mock_session, send_opts)
