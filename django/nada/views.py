from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Neuron, Synapse

        
# S1
@api_view(['GET'])
def is_synapse(request, collection=None, experiment=None, layer=None, id=None):
    synapse = Synapse.get_by_celi(collection, experiment, layer, id)
    result = { "result": not (synapse == None) }
    return Response(result, status=status.HTTP_200_OK)

# S5
@api_view(['GET'])
def is_neuron(request, collection=None, experiment=None, layer=None, id=None):
    neuron = Neuron.get_by_celi(collection, experiment, layer, id)
    result = { "result": not (neuron == None) }
    return Response(result, status=status.HTTP_200_OK)


# S2
@api_view(['GET'])
def synapse_ids(request, collection=None, experiment=None, layer=None, resolution=None,
                           x_start=None, x_stop=None,
                           y_start=None, y_stop=None,
                           z_start=None, z_stop=None
                           ):
    result = { "ids": ['123', '456', '999'] }
    return Response(result, status=status.HTTP_200_OK)

# S6
@api_view(['GET'])
def neuron_ids(request, collection=None, experiment=None, layer=None, resolution=None,
                           x_start=None, x_stop=None,
                           y_start=None, y_stop=None,
                           z_start=None, z_stop=None
                           ):
    result = { "ids": ['123', '456', '999'] }
    return Response(result, status=status.HTTP_200_OK)

# S3 
@api_view(['GET'])
def synapse_keypoint(request, collection=None, experiment=None, layer=None, resolution=None, id=None):
    result = { "keypoint": [10, 10, 10] }
    return Response(result, status=status.HTTP_200_OK)

# S7
@api_view(['GET'])
def neuron_keypoint(request, collection=None, experiment=None, layer=None, resolution=None, id=None):
    result = { "keypoint": [10, 10, 10] }
    return Response(result, status=status.HTTP_200_OK)

# S4
@api_view(['GET'])
def synapse_parent(request, collection=None, experiment=None, layer=None, id=None):
    result = { "parent_neurons": { '12345': 1, '34567': 2 } }
    return Response(result, status=status.HTTP_200_OK)

# S8
@api_view(['GET'])
def neuron_children(request, collection=None, experiment=None, layer=None,  resolution=None,
                        x_start=None, x_stop=None,
                        y_start=None, y_stop=None,
                        z_start=None, z_stop=None, id=None):
    result = { "child_synapses": { '12345': 1, '34567': 2 } }
    return Response(result, status=status.HTTP_200_OK)


# S9
@api_view(['GET'])
def voxel_list(request, collection=None, experiment=None, layer=None,  resolution=None,
                        x_start=None, x_stop=None,
                        y_start=None, y_stop=None,
                        z_start=None, z_stop=None, id=None):
    result = { "x": [0, 0, 0, 1, 1, 1],
               "y": [1, 0, 1, 0, 1, 0],
               "z": [1, 2, 3, 1, 2, 3] }
    return Response(result, status=status.HTTP_200_OK)
