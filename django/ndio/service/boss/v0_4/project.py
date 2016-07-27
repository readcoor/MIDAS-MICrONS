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

from .base import Base
from ndio.ndresource.boss.resource import *
from requests import HTTPError
import copy

class ProjectService_0_4(Base):
    """The Boss API v0.4 project service.
    """

    def __init__(self):
        super().__init__()

    @property
    def endpoint(self):
        return 'resource'

    def list(self, resource, url_prefix, auth, session, send_opts):
        """List all resources of the same type as the given resource.

        Args:
            resource (ndio.ndresource.boss.Resource): List resources of the same type as this..
            url_prefix (string): Protocol + host such as https://api.theboss.io
            auth (string): Token to send in the request header.
            session (requests.Session): HTTP session to use for request.
            send_opts (dictionary): Additional arguments to pass to session.send().

        Returns:
            (list): List of resources.  Each resource is a dictionary.

        Raises:
            requests.HTTPError on failure.
        """
        req = self.get_request(
            resource, 'GET', 'application/x-www-form-urlencoded', url_prefix, auth,
            proj_list_req = True)
            # json content-type currently broken.
            #resource, 'GET', 'application/json', url_prefix, auth,
            #proj_list_req = True)
        prep = session.prepare_request(req)
        resp = session.send(prep, **send_opts)
        if resp.status_code == 200:
            return resp.json()

        err = ('List failed on {}, got HTTP response: ({}) - {}'.format(
            resource.name, resp.status_code, resp.text))
        raise HTTPError(err, request = req, response = resp)

    def create(self, resource, url_prefix, auth, session, send_opts):
        """Create the given resource.

        Args:
            resource (ndio.ndresource.boss.Resource): Create a data model object with attributes matching those of the resource.
            url_prefix (string): Protocol + host such as https://api.theboss.io
            auth (string): Token to send in the request header.
            session (requests.Session): HTTP session to use for request.
            send_opts (dictionary): Additional arguments to pass to session.send().

        Returns:
            (ndio.ndresource.boss.Resource): Returns resource of type requested on success.  Returns None on failure.

        Raises:
            requests.HTTPError on failure.
        """
        json = self._get_resource_params(resource)
        req = self.get_request(
            resource, 'POST', 'application/x-www-form-urlencoded', url_prefix, auth,
            data = json)
            # json content-type currently broken.
            #resource, 'POST', 'application/json', url_prefix, auth,
            #json = json)
        prep = session.prepare_request(req)
        resp = session.send(prep, **send_opts)

        if resp.status_code == 201:
            return self._create_resource_from_dict(resource, resp.json())

        err = ('Create failed on {}, got HTTP response: ({}) - {}'.format(
            resource.name, resp.status_code, resp.text))
        raise HTTPError(err, request = req, response = resp)

    def get(self, resource, url_prefix, auth, session, send_opts):
        """Get attributes of the given resource.

        Args:
            resource (ndio.ndresource.boss.Resource): Create a data model object with attributes matching those of the resource.
            url_prefix (string): Protocol + host such as https://api.theboss.io
            auth (string): Token to send in the request header.
            session (requests.Session): HTTP session to use for request.
            send_opts (dictionary): Additional arguments to pass to session.send().

        Returns:
            (ndio.resource.boss.Resource): Returns resource of type requested on success.  Returns None on failure.

        Raises:
            requests.HTTPError on failure.
        """
        req = self.get_request(
            resource, 'GET', 'application/json', url_prefix, auth)
        prep = session.prepare_request(req)
        resp = session.send(prep, **send_opts)
        if resp.status_code == 200:
            return self._create_resource_from_dict(resource, resp.json())

        err = ('Get failed on {}, got HTTP response: ({}) - {}'.format(
            resource.name, resp.status_code, resp.text))
        raise HTTPError(err, request = req, response = resp)

    def update(self, resource_name, resource, url_prefix, auth, session, send_opts):
        """Updates an entity in the data model using the given resource.

        Args:
            resource_name (string): Current name of the resource (in case the resource is getting its name changed).
            resource (ndio.resource.boss.Resource): New attributes for the resource.
            url_prefix (string): Protocol + host such as https://api.theboss.io
            auth (string): Token to send in the request header.
            session (requests.Session): HTTP session to use for request.
            send_opts (dictionary): Additional arguments to pass to session.send().

        Returns:
            (ndio.resource.boss.Resource): Returns updated resource of given type on success.  Returns None on failure.

        Raises:
            requests.HTTPError on failure.
        """

        # Create a copy of the resource and change its name to resource_name
        # in case the update includes changing the name of a resource.
        old_resource = copy.deepcopy(resource)
        old_resource.name = resource_name

        json = self._get_resource_params(resource, for_update=True)

        req = self.get_request(
            old_resource, 'PUT', 'application/x-www-form-urlencoded',
            url_prefix, auth, data = json)
            # json content-type currently broken.
            #old_resource, 'PUT', 'application/json', url_prefix, auth,
            #json = json)
        prep = session.prepare_request(req)
        resp = session.send(prep, **send_opts)

        if resp.status_code == 200:
            return self._create_resource_from_dict(resource, resp.json())

        err = ('Update failed on {}, got HTTP response: ({}) - {}'.format(
            old_resource.name, resp.status_code, resp.text))
        raise HTTPError(err, request = req, response = resp)


    def delete(self, resource, url_prefix, auth, session, send_opts):
        """Deletes the entity described by the given resource.

        Args:
            resource (ndio.resource.boss.Resource)
            url_prefix (string): Protocol + host such as https://api.theboss.io
            auth (string): Token to send in the request header.
            session (requests.Session): HTTP session to use for request.
            send_opts (dictionary): Additional arguments to pass to session.send().

        Raises:
            requests.HTTPError on failure.
        """
        req = self.get_request(
            resource, 'DELETE', 'application/json', url_prefix, auth)
        prep = session.prepare_request(req)
        resp = session.send(prep, **send_opts)
        if resp.status_code == 204:
            return

        err = ('Delete failed on {}, got HTTP response: ({}) - {}'.format(
            resource.name, resp.status_code, resp.text))
        raise HTTPError(err, request = req, response = resp)

    def _get_resource_params(self, resource, for_update=False):
        """Get dictionary containing all parameters for the given resource.

        When getting params for a coordinate frame update, only name and 
        description are returned because they are the only fields that can
        be updated.

        Args:
            resource (ndio.ndresource.boss.resource.Resource): A sub-class
                whose parameters will be extracted into a dictionary.
            for_update (bool): True if params will be used for an update.

        Returns:
            (dictionary): A dictionary containing the resource's parameters as
            required by the Boss API.

        Raises:
            TypeError if resource is not a supported class.
        """
        if isinstance(resource, CollectionResource):
            return self._get_collection_params(resource)

        if isinstance(resource, ExperimentResource):
            return self._get_experiment_params(resource)

        if isinstance(resource, CoordinateFrameResource):
            return self._get_coordinate_params(resource, for_update)

        if isinstance(resource, LayerResource):
            return self._get_layer_params(resource)

        if isinstance(resource, ChannelResource):
            return self._get_channel_params(resource)

        raise TypeError('resource is not supported type.')

    def _get_collection_params(self, coll):
        return { 'name': coll.name, 'description': coll.description }

    def _get_experiment_params(self, exp):
        return {
            'name': exp.name,
            'description': exp.description ,
            'coord_frame': exp.coord_frame,
            'num_hierarchy_levels': exp.num_hierarchy_levels,
            'hierarchy_method': exp.hierarchy_method,
            'max_time_sample': exp.max_time_sample
        }

    def _get_coordinate_params(self, coord, for_update):
        if not for_update:
            return {
                'name': coord.name,
                'description': coord.description ,
                'x_start': coord.x_start,
                'x_stop': coord.x_stop,
                'y_start': coord.y_start,
                'y_stop': coord.y_stop,
                'z_start': coord.z_start,
                'z_stop': coord.z_stop,
                'x_voxel_size': coord.x_voxel_size,
                'y_voxel_size': coord.y_voxel_size,
                'z_voxel_size': coord.z_voxel_size,
                'voxel_unit': coord.voxel_unit,
                'time_step': coord.time_step,
                'time_step_unit': coord.time_step_unit
            }

        return { 'name': coord.name, 'description': coord.description }

    def _get_channel_params(self, chan):
        return {
            'name': chan.name,
            'description': chan.description ,
            'default_time_step': chan.default_time_step,
            'datatype': chan.datatype,
            'base_resolution': chan.base_resolution,
            'is_channel': True
        }

    def _get_layer_params(self, lyr):
        return {
            'name': lyr.name,
            'description': lyr.description ,
            'default_time_step': lyr.default_time_step,
            'datatype': lyr.datatype,
            'base_resolution': lyr.base_resolution,
            'is_channel': False,
            'channels': lyr.channels
        }

    def _create_resource_from_dict(self, resource, dict):
        """
        Args:
            resource (ndio.resource.boss.Resource): Used to determine type of resource to create.
            dict (dictionary): JSON data returned by the Boss API.

        Returns:
            (ndio.resource.boss.Resource): Instance populated with values from dict.

        Raises:
            KeyError if dict missing required key.
            TypeError if resource is not a supported class.
        """
        if isinstance(resource, CollectionResource):
            return self._get_collection(dict)

        if isinstance(resource, ExperimentResource):
            return self._get_experiment(dict, resource.coll_name)

        if isinstance(resource, CoordinateFrameResource):
            return self._get_coordinate(dict)

        if isinstance(resource, LayerResource):
            return self._get_layer(dict, resource.coll_name, resource.exp_name)

        if isinstance(resource, ChannelResource):
            return self._get_channel(dict, resource.coll_name, resource.exp_name)

        raise TypeError('resource is not supported type.')

    def _get_collection(self, dict):
        name = dict['name']
        description = dict['description']
        id = dict['id']
        creator = dict['creator']
        return CollectionResource(
            name, self.version, description, id, creator, raw=dict)

    def _get_experiment(self, dict, coll_name):
        exp_keys = [
            'id', 'name', 'description', 'creator', 'coord_frame', 
            'num_hierarchy_levels', 'hierarchy_method', 'max_time_sample'             
        ]

        filtered = { k:v for (k, v) in dict.items() if k in exp_keys }
        return ExperimentResource(
            version=self.version, collection_name=coll_name, raw=dict, **filtered)

    def _get_coordinate(self, dict):
        coord_keys = [
            'id', 'name', 'description', 'x_start', 'x_stop', 
            'y_start', 'y_stop', 'z_start', 'z_stop', 
            'x_voxel_size', 'y_voxel_size', 'z_voxel_size',
            'voxel_unit', 'time_step', 'time_step_unit'
        ]

        filtered = { k:v for (k, v) in dict.items() if k in coord_keys }
        return CoordinateFrameResource(version=self.version, raw=dict, **filtered)

    def _get_channel(self, dict, coll_name, exp_name):
        chan_keys = [
            'id', 'name', 'description', 'creator', 'default_time_step', 
            'datatype', 'base_resolution'
        ]

        filtered = { k:v for (k, v) in dict.items() if k in chan_keys }
        collection = coll_name
        return ChannelResource(
            version=self.version, collection_name=collection,
            experiment_name=exp_name, raw=dict, **filtered)

    def _get_layer(self, dict, coll_name, exp_name):
        layer_keys = [
            'id', 'name', 'description', 'creator', 'default_time_step', 
            'datatype', 'base_resolution'
        ]

        filtered = { k:v for (k, v) in dict.items() if k in layer_keys }
        collection = coll_name
        channels = dict['linked_channel_layers']
        return LayerResource(
            version=self.version, collection_name=collection,
            experiment_name=exp_name, channels=channels, raw=dict, **filtered)
