from django.conf.urls import url
from . import views

urlpatterns = [ 
    url(r'^is_synapse/$', views.is_synapse, name='is_synapse'),
    url(r'^is_neuron/$', views.is_neuron, name='is_neuron'),
    url(r'^synapse_ids/$', views.synapse_ids, name='synapse_ids'),
    url(r'^neuron_ids/$', views.neuron_ids, name='neuron_ids'),
    url(r'^synapse_keypoint/$', views.synapse_keypoint, name='synapse_keypoint'),
    url(r'^neuron_keypoint/$', views.neuron_keypoint, name='neuron_keypoint'),
    url(r'^synapse_parent/$', views.synapse_parent, name='synapse_parent'),
    url(r'^neuron_children/$', views.neuron_children, name='neuron_children'),
]
