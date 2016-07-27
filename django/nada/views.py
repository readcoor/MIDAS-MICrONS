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


def bounded_view(cls, table_name, x_start, y_start, z_start, x_stop, y_stop, z_stop):
    '''
    Returns a query of objects (specified by cls, table_name)
    within a bounded volume.
    '''
    box = 'ST_3DMakeBox(ST_MakePoint(%s,%s,%s),ST_MakePoint(%s,%s,%s))' % \
          (x_start, y_start, z_start, x_stop, y_stop, z_stop)
    query = 'select id from %s as s where s.keypoint &&& %s;' % (table_name, box)
    return cls.objects.raw(query)

# S2
@api_view(['GET'])
def synapse_ids(request, collection=None, experiment=None, layer=None, resolution=None,
                           x_start=None, x_stop=None,
                           y_start=None, y_stop=None,
                           z_start=None, z_stop=None
                           ):
    '''
    TODO: does not filter for CELI just yet.
    '''
    view = bounded_view(Synapse, 'nada_synapse', x_start, y_start, z_start, x_stop, y_stop, z_stop)
    result = { "ids": [obj.name for obj in view] }
    return Response(result, status=status.HTTP_200_OK)

# S6
@api_view(['GET'])
def neuron_ids(request, collection=None, experiment=None, layer=None, resolution=None,
                           x_start=None, x_stop=None,
                           y_start=None, y_stop=None,
                           z_start=None, z_stop=None
                           ):
    '''
    TODO: does not filter for CELI just yet.
    '''
    view = bounded_view(Neuron, 'nada_neuron', x_start, y_start, z_start, x_stop, y_stop, z_stop)
    result = { "ids": [obj.name for obj in view] }
    return Response(result, status=status.HTTP_200_OK)

# S3 
@api_view(['GET'])
def synapse_keypoint(request, collection=None, experiment=None, layer=None, resolution=None, id=None):
    synapse = Synapse.get_by_celi(collection, experiment, layer, id)
    if synapse:
        result = { "keypoint": synapse.keypoint.coords }
        return Response(result, status=status.HTTP_200_OK)
    err_msg = "Not found: %s with collection=%s, experiment=%s, layer=%s, resolution=%s, id=%s" % \
              ('synapse', collection, experiment, layer, resolution, id)
    return Response(err_msg, status.HTTP_404_NOT_FOUND)

# S7
@api_view(['GET'])
def neuron_keypoint(request, collection=None, experiment=None, layer=None, resolution=None, id=None):
    neuron = Neuron.get_by_celi(collection, experiment, layer, id)
    if neuron:
        result = { "keypoint": neuron.keypoint.coords }
        return Response(result, status=status.HTTP_200_OK)
    err_msg = "Not found: %s with collection=%s, experiment=%s, layer=%s, resolution=%s, id=%s" % \
              ('neuron', collection, experiment, layer, resolution, id)
    return Response(err_msg, status.HTTP_404_NOT_FOUND)


# S4
@api_view(['GET'])
def synapse_parent(request, collection=None, experiment=None, layer=None, id=None):
    synapse = Synapse.get_by_celi(collection, experiment, layer, id)
    if synapse:
        neurons = {}
        neuron1 = synapse.neuron
        if neuron1:
            neurons[neuron1.name] = synapse.polarity
        neuron2 = synapse.partner_neuron
        if neuron2:
            partner = synapse.partner_synapse
            if partner:
                neurons[neuron2.name] = partner.polarity
        result = { "parent_neurons": neurons }
        return Response(result, status=status.HTTP_200_OK)
    err_msg = "Not found: %s with collection=%s, experiment=%s, layer=%s, id=%s" % (collection, experiment, layer, id)
    return Response(err_msg, status.HTTP_404_NOT_FOUND)

# S8
@api_view(['GET'])
def neuron_children(request, collection=None, experiment=None, layer=None,  resolution=None,
                        x_start=None, x_stop=None,
                        y_start=None, y_stop=None,
                        z_start=None, z_stop=None, id=None):
    neuron = Neuron.get_by_celi(collection, experiment, layer, id)
    if neuron:
        result = { "child_synapses": dict([(s.name, s.polarity) for s in neuron.synapses.all() ]) }
        return Response(result, status=status.HTTP_200_OK)
    err_msg = "Not found: %s with collection=%s, experiment=%s, layer=%s, id=%s" % (collection, experiment, layer, id)
    return Response(err_msg, status.HTTP_404_NOT_FOUND)


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
