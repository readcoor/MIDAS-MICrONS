from django.conf.urls import url
from . import views


def param(name):
    if isinstance(name, list):
        return ','.join(['(?P<%s>[\w_-]+)' % elt for elt in name])
    return '(?P<%s>[\w_-]+)' % name

def params(*names):
    return '/'.join([param(name) for name in names])

urlpatterns = [ 
    url(r'^is_synapse/' + params('collection', 'experiment', 'layer', 'id') + r'/?$',
        views.is_synapse, name='is_synapse'),
    url(r'^is_neuron/' + params('collection', 'experiment', 'layer', 'id') + r'/?$',
        views.is_neuron, name='is_neuron'),
    url(r'^synapse_ids/' + params('collection', 'experiment', 'layer', 'resolution',
                                  ['x_start', 'x_stop'],
                                  ['y_start', 'y_stop'],
                                  ['z_start', 'z_stop']) + r'/?$',
        views.synapse_ids, name='synapse_ids'),
    url(r'^neuron_ids/' + params('collection', 'experiment', 'layer', 'resolution',
                                 ['x_start', 'x_stop'],
                                 ['y_start', 'y_stop'],
                                 ['z_start', 'z_stop']) + r'/?$', 
        views.neuron_ids, name='neuron_ids'),
    url(r'^synapse_keypoint/' + params('collection', 'experiment', 'layer', 'resolution', 'id') + r'/?$',
        views.synapse_keypoint, name='synapse_keypoint'),
    url(r'^neuron_keypoint/' + params('collection', 'experiment', 'layer', 'resolution', 'id') + r'/?$',
        views.neuron_keypoint, name='neuron_keypoint'),
    url(r'^synapse_parent/' + params('collection', 'experiment', 'layer', 'id') + r'/?$',
        views.synapse_parent, name='synapse_parent'),           
    url(r'^neuron_children/' + params('collection', 'experiment', 'layer', 'resolution',
                                      ['x_start', 'x_stop'],
                                      ['y_start', 'y_stop'],
                                      ['z_start', 'z_stop'],
                                      'id') + r'/?$',
        views.neuron_children, name='neuron_children'),
    url(r'^voxel_list/' + params('collection', 'experiment', 'layer', 'resolution',
                                 ['x_start', 'x_stop'],
                                 ['y_start', 'y_stop'],
                                 ['z_start', 'z_stop'], 'id') + r'/?$', 
        views.voxel_list, name='voxel_list')
]
