# Copyright 2016 Wyss Institute
# portions Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from . import Collection, Experiment, Channel, CoordinateFrame

__all__ = [ 'CollectionSerializer', 'ExperimentSerializer', 
            'CoordinateFrameSerializer', 'ChannelSerializer' ]

class CollectionSerializer(serializers.ModelSerializer):
    #experiments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='experiment-detail')

    class Meta:
        model = Collection
        #fields = ('id', 'name', 'description', 'experiments')

class ExperimentSerializer(serializers.ModelSerializer):
    #channels = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='channel-detail')

    class Meta:
        model = Experiment
        #fields = ('id', 'name', 'description', 'collection', 'coord_frame', 'num_hierarchy_levels', 'hierarchy_method',
        #          'max_time_sample', 'channels')
        #extra_kwargs = {'collection': {'lookup_field': 'name', 'lookup_url_kwarg':'collection'},
        #                'coord_frame': {'lookup_field': 'name', 'lookup_url_kwarg':'coord_frame'}}

class CoordinateFrameSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoordinateFrame
        #fields = ('id', 'name', 'description', 'x_start', 'x_stop', 'y_start', 'y_stop', 'z_start', 'z_stop',
        #          'x_voxel_size', 'y_voxel_size', 'z_voxel_size', 'voxel_unit', 'time_step', 'time_step_unit')

class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        #fields = ('id', 'name', 'description', 'is_channel', 'experiment', 'default_time_step',
        #          'base_resolution', 'datatype')
