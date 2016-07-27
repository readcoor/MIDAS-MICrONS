﻿# Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
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

from ndio.service.boss.v0_5.project import ProjectService_0_5
from ndio.ndresource.boss.resource import *
from requests import HTTPError, PreparedRequest, Response, Session
import unittest
from unittest.mock import patch

class TestProject_v0_5(unittest.TestCase):
    def setUp(self):
        self.prj = ProjectService_0_5()
        self.chan = ChannelResource('chan', 'foo', 'bar', datatype='uint16')

    @patch('requests.Response', autospec=True)
    @patch('requests.Session', autospec=True)
    def test_prj_list_success(self, mock_session, mock_resp):
        expected = [{'name': 'foo'}, {'name': 'bar'}]
        mock_session.prepare_request.return_value = PreparedRequest()
        mock_resp.status_code = 200
        mock_resp.json.return_value = expected

        mock_session.send.return_value = mock_resp

        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'
        send_opts = {}

        actual = self.prj.list(self.chan, url_prefix, auth, mock_session, send_opts)

        self.assertEqual(expected, actual)

    @patch('requests.Response', autospec=True)
    @patch('requests.Session', autospec=True)
    def test_prj_list_failure(self, mock_session, mock_resp):
        mock_session.prepare_request.return_value = PreparedRequest()
        mock_resp.status_code = 403
        mock_resp.raise_for_status.side_effect = HTTPError()

        mock_session.send.return_value = mock_resp

        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'
        send_opts = {}

        with self.assertRaises(HTTPError):
            self.prj.list(self.chan, url_prefix, auth, mock_session, send_opts)

    @patch('requests.Response', autospec=True)
    @patch('requests.Session', autospec=True)
    def test_prj_create_success(self, mock_session, mock_resp):
        mock_session.prepare_request.return_value = PreparedRequest()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {
            'id': 7, 'name': 'chan', 'description': 'walker', 
            'experiment': 'bar', 'creator': 'me',
            'default_time_step': 2, 'datatype': 'uint16', 'base_resolution': 0
        }

        mock_session.send.return_value = mock_resp

        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'
        send_opts = {}

        actual = self.prj.create(self.chan, url_prefix, auth, mock_session, send_opts)

        self.assertTrue(isinstance(actual, ChannelResource))
        self.assertEqual('chan', actual.name)
        self.assertEqual('foo', actual.coll_name)
        self.assertEqual('bar', actual.exp_name)

    @patch('requests.Session', autospec=True)
    def test_prj_create_failure(self, mock_session):
        mock_session.prepare_request.return_value = PreparedRequest()
        fake_resp = Response()
        fake_resp.status_code = 403

        mock_session.send.return_value = fake_resp

        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'
        send_opts = {}

        with self.assertRaises(HTTPError):
            self.prj.create(self.chan, url_prefix, auth, mock_session, send_opts)

    @patch('requests.Response', autospec=True)
    @patch('requests.Session', autospec=True)
    def test_prj_get_success(self, mock_session, mock_resp):
        chan_dict = { 
            'id': 10, 'name': 'bar', 'description': 'none', 'experiment': 8, 
            'is_channel': True, 'default_time_step': 0, 'datatype': 'uint16',
            'base_resolution': 0, 'linked_channel_layers': [], 'creator': 'me'
        }
        expected = ChannelResource(
            chan_dict['name'], self.chan.coll_name, self.chan.exp_name) 
        expected.description = chan_dict['description']
        expected.datatype = chan_dict['datatype']
        expected.base_resolution = chan_dict['base_resolution']
        expected.default_time_step = chan_dict['default_time_step']
        expected.id = chan_dict['id']


        mock_session.prepare_request.return_value = PreparedRequest()
        mock_resp.json.return_value = chan_dict
        mock_resp.status_code = 200

        mock_session.send.return_value = mock_resp

        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'
        send_opts = {}

        actual = self.prj.get(self.chan, url_prefix, auth, mock_session, send_opts)

        self.assertEqual(expected.name, actual.name)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.description, actual.description)
        self.assertEqual(expected.exp_name, actual.exp_name)
        self.assertEqual(expected.coll_name, actual.coll_name)
        self.assertEqual(expected.default_time_step, actual.default_time_step)
        self.assertEqual(expected.datatype, actual.datatype)
        self.assertEqual(expected.base_resolution, actual.base_resolution)

    @patch('requests.Response', autospec=True)
    @patch('requests.Session', autospec=True)
    def test_prj_get_failure(self, mock_session, mock_resp):
        mock_session.prepare_request.return_value = PreparedRequest()
        mock_resp.status_code = 403
        mock_resp.raise_for_status.side_effect = HTTPError()

        mock_session.send.return_value = mock_resp

        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'
        send_opts = {}

        with self.assertRaises(HTTPError):
            self.prj.get(self.chan, url_prefix, auth, mock_session, send_opts)

    @patch('requests.Response', autospec=True)
    @patch('requests.Session', autospec=True)
    def test_prj_update_success(self, mock_session, mock_resp):
        chan_dict = { 
            'id': 10, 'name': 'bar', 'description': 'none', 'experiment': 8, 
            'is_channel': True, 'default_time_step': 0, 'datatype': 'uint16',
            'base_resolution': 0, 'linked_channel_layers': [], 'creator': 'me'
        }
        expected = ChannelResource(
            chan_dict['name'], self.chan.coll_name, self.chan.exp_name) 
        expected.description = chan_dict['description']
        expected.datatype = chan_dict['datatype']
        expected.base_resolution = chan_dict['base_resolution']
        expected.default_time_step = chan_dict['default_time_step']
        expected.id = chan_dict['id']

        mock_session.prepare_request.return_value = PreparedRequest()
        mock_resp.json.return_value = chan_dict
        mock_resp.status_code = 200

        mock_session.send.return_value = mock_resp

        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'
        send_opts = {}

        actual = self.prj.update(self.chan.name, self.chan, url_prefix, auth, mock_session, send_opts)

        self.assertEqual(expected.name, actual.name)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.description, actual.description)
        self.assertEqual(expected.exp_name, actual.exp_name)
        self.assertEqual(expected.coll_name, actual.coll_name)
        self.assertEqual(expected.default_time_step, actual.default_time_step)
        self.assertEqual(expected.datatype, actual.datatype)
        self.assertEqual(expected.base_resolution, actual.base_resolution)

    @patch('requests.Session', autospec=True)
    def test_prj_update_failure(self, mock_session):
        mock_session.prepare_request.return_value = PreparedRequest()
        fake_resp = Response()
        fake_resp.status_code = 403

        mock_session.send.return_value = fake_resp

        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'
        send_opts = {}

        with self.assertRaises(HTTPError):
            self.prj.update(self.chan.name, self.chan, url_prefix, auth, mock_session, send_opts)

    @patch('requests.Session', autospec=True)
    def test_prj_delete_success(self, mock_session):
        mock_session.prepare_request.return_value = PreparedRequest()
        fake_resp = Response()
        fake_resp.status_code = 204

        mock_session.send.return_value = fake_resp

        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'
        send_opts = {}

        self.prj.delete(self.chan, url_prefix, auth, mock_session, send_opts)

    @patch('requests.Session', autospec=True)
    def test_prj_delete_failure(self, mock_session):
        mock_session.prepare_request.return_value = PreparedRequest()
        fake_resp = Response()
        fake_resp.status_code = 403

        mock_session.send.return_value = fake_resp

        url_prefix = 'https://api.theboss.io'
        auth = 'mytoken'
        send_opts = {}

        with self.assertRaises(HTTPError):
            self.prj.delete(self.chan, url_prefix, auth, mock_session, send_opts)

    def test_get_resource_params_bad_type(self):
        with self.assertRaises(TypeError):
            self.prj._get_resource_params(None)

    def test_get_resource_params_collection(self):
        coll = CollectionResource('foo')
        actual = self.prj._get_resource_params(coll)
        self.assertEqual('foo', actual['name'])
        self.assertTrue('description' in actual)

    def test_get_resource_params_experiment(self):
        exp = ExperimentResource('foo', 'coll')
        actual = self.prj._get_resource_params(exp)
        self.assertEqual('foo', actual['name'])
        self.assertTrue('description' in actual)
        self.assertTrue('coord_frame' in actual)
        self.assertTrue('num_hierarchy_levels' in actual)
        self.assertTrue('hierarchy_method' in actual)
        self.assertTrue('max_time_sample' in actual)

    def test_get_resource_params_coord_frame_for_update(self):

        coord = CoordinateFrameResource('foo')
        actual = self.prj._get_resource_params(coord, for_update=True)
        self.assertEqual('foo', actual['name'])
        self.assertTrue('description' in actual)
        self.assertEqual(2, len(actual))

    def test_get_resource_params_coord_frame(self):
        coord = CoordinateFrameResource('foo')
        actual = self.prj._get_resource_params(coord, for_update=False)
        self.assertEqual('foo', actual['name'])
        self.assertTrue('description' in actual)
        self.assertTrue('x_start' in actual)
        self.assertTrue('x_stop' in actual)
        self.assertTrue('y_start' in actual)
        self.assertTrue('y_stop' in actual)
        self.assertTrue('z_start' in actual)
        self.assertTrue('z_stop' in actual)
        self.assertTrue('x_voxel_size' in actual)
        self.assertTrue('y_voxel_size' in actual)
        self.assertTrue('z_voxel_size' in actual)
        self.assertTrue('voxel_unit' in actual)
        self.assertTrue('time_step' in actual)
        self.assertTrue('time_step_unit' in actual)

    def test_get_resource_params_channel(self):
        chan = ChannelResource('foo', 'coll', 'exp')
        actual = self.prj._get_resource_params(chan)
        self.assertEqual('foo', actual['name'])
        self.assertTrue(actual['is_channel'])
        self.assertTrue('description' in actual)
        self.assertTrue('default_time_step' in actual)
        self.assertTrue('datatype' in actual)
        self.assertTrue('base_resolution' in actual)

    def test_get_resource_params_layer(self):
        layer = LayerResource('foo', 'coll', 'exp')
        actual = self.prj._get_resource_params(layer)
        self.assertEqual('foo', actual['name'])
        self.assertFalse(actual['is_channel'])
        self.assertTrue('description' in actual)
        self.assertTrue('default_time_step' in actual)
        self.assertTrue('datatype' in actual)
        self.assertTrue('base_resolution' in actual)
        self.assertTrue('channels' in actual)

    def test_create_resource_from_dict_bad_type(self):
        bad_type = self.prj
        dict = {}
        with self.assertRaises(TypeError):
            self.prj._create_resource_from_dict(bad_type, dict)

    def test_create_resource_from_dict_collection(self):
        coll = CollectionResource('')
        dict = { 'name': 'fire', 'description': 'walker', 'id': 5, 'creator': 'auto' }
        actual = self.prj._create_resource_from_dict(coll, dict)
        self.assertEqual('fire', actual.name)
        self.assertEqual('walker', actual.description)
        self.assertEqual(5, actual.id)
        self.assertEqual('auto', actual.creator)
        self.assertEqual(self.prj.version, actual.version)
        self.assertEqual(dict, actual.raw)

    def test_create_resource_from_dict_experiment(self):
        exp = ExperimentResource('', 'pyro')
        dict = { 
            'name': 'fire', 'description': 'walker', 
            'id': 5, 'creator': 'auto', 'coord_frame': 3, 
            'num_hierarchy_levels': 1, 'hierarchy_method': 'near_iso',
            'max_time_sample': 500
        }

        actual = self.prj._create_resource_from_dict(exp, dict)
        self.assertEqual('fire', actual.name)
        self.assertEqual('walker', actual.description)
        self.assertEqual(5, actual.id)
        self.assertEqual('auto', actual.creator)
        self.assertEqual(3, actual.coord_frame)
        self.assertEqual(1, actual.num_hierarchy_levels)
        self.assertEqual('near_iso', actual.hierarchy_method)
        self.assertEqual(500, actual.max_time_sample)
        self.assertEqual('pyro', actual.coll_name)
        self.assertEqual(self.prj.version, actual.version)
        self.assertEqual(dict, actual.raw)

    def test_create_resource_from_dict_coordinate(self):
        coord = CoordinateFrameResource('')
        dict = {
            'id': 7, 'name': 'fire', 'description': 'walker', 
            'x_start': 0, 'x_stop': 100, 
            'y_start': 50, 'y_stop': 150, 'z_start': 75, 'z_stop': 125, 
            'x_voxel_size': 2, 'y_voxel_size': 4, 'z_voxel_size': 6,
            'voxel_unit': 'centimeters', 
            'time_step': 2, 'time_step_unit': 'milliseconds'}

        actual = self.prj._create_resource_from_dict(coord, dict)
        self.assertEqual('fire', actual.name)
        self.assertEqual('walker', actual.description)
        self.assertEqual(7, actual.id)
        self.assertEqual(0, actual.x_start)
        self.assertEqual(100, actual.x_stop)
        self.assertEqual(50, actual.y_start)
        self.assertEqual(150, actual.y_stop)
        self.assertEqual(75, actual.z_start)
        self.assertEqual(125, actual.z_stop)
        self.assertEqual(2, actual.x_voxel_size)
        self.assertEqual(4, actual.y_voxel_size)
        self.assertEqual(6, actual.z_voxel_size)
        self.assertEqual('centimeters', actual.voxel_unit)
        self.assertEqual(2, actual.time_step)
        self.assertEqual('milliseconds', actual.time_step_unit)
        self.assertEqual(dict, actual.raw)

    def test_create_resource_from_dict_channel(self):
        chan = ChannelResource('', 'coll1', 'exp1')
        dict = {
            'id': 7, 'name': 'fire', 'description': 'walker', 
            'experiment': 'exp1', 'creator': 'me',
            'default_time_step': 2, 'datatype': 'uint16', 'base_resolution': 0
        }

        actual = self.prj._create_resource_from_dict(chan, dict)
        self.assertEqual('fire', actual.name)
        self.assertEqual('walker', actual.description)
        self.assertEqual(7, actual.id)
        self.assertEqual('coll1', actual.coll_name)
        self.assertEqual('exp1', actual.exp_name)
        self.assertEqual('me', actual.creator)
        self.assertEqual(2, actual.default_time_step)
        self.assertEqual('uint16', actual.datatype)
        self.assertEqual(0, actual.base_resolution)
        self.assertEqual(dict, actual.raw)

    def test_create_resource_from_dict_layer(self):
        layer = LayerResource('', 'coll1', 'exp1')
        dict = {
            'id': 7, 'name': 'fire', 'description': 'walker', 
            'experiment': 'exp1', 'creator': 'me',
            'default_time_step': 2, 'datatype': 'uint16', 'base_resolution': 0,
            'linked_channel_layers': [10, 12]
        }

        actual = self.prj._create_resource_from_dict(layer, dict)
        self.assertEqual('fire', actual.name)
        self.assertEqual('walker', actual.description)
        self.assertEqual(7, actual.id)
        self.assertEqual('coll1', actual.coll_name)
        self.assertEqual('exp1', actual.exp_name)
        self.assertEqual('me', actual.creator)
        self.assertEqual(2, actual.default_time_step)
        self.assertEqual('uint16', actual.datatype)
        self.assertEqual(0, actual.base_resolution)
        self.assertEqual([10, 12], actual.channels)
        self.assertEqual(dict, actual.raw)

if __name__ == '__main__':
    unittest.main()

