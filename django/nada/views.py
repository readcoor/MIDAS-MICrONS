from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Neuron, Synapse, Compartment, CellType, NeuronStimulus, NeuronActivity
from .boss_client import BossClient

from psycopg2.extensions import adapt as esc

def num(s):
    '''make sure input is a number'''
    try:
        return int(s)
    except ValueError:
        return float(s)
        
def filtered_query(cls, collection, experiment, layer,
                   x_start, y_start, z_start, x_stop, y_stop, z_stop,
                   id=None):
    '''
    Returns a query to find objects (of class==cls) within a bounded volume.
    Filter for only objects belonging to the given collection/experiment/layer.
    If ID is provided, also filter for only objects with that name. 
    '''
    table_name = cls._meta.db_table

    # escape for sql injection
    (collection_e, experiment_e, layer_e) = (esc(collection), esc(experiment), esc(layer))

    # ensure numeric values for xyz start/stop boundaries
    (x_start_n, y_start_n, z_start_n, x_stop_n, y_stop_n, z_stop_n) = \
                [num(s) for s in [x_start, y_start, z_start, x_stop, y_stop, z_stop]]

    box = 'ST_3DMakeBox(ST_MakePoint(%s,%s,%s),ST_MakePoint(%s,%s,%s))' % \
          (x_start_n, y_start_n, z_start_n, x_stop_n, y_stop_n, z_stop_n)

    query = 'SELECT n.id FROM %s n, nada_experiment e, nada_collection c, nada_layer l' % table_name
    query += ' where n.keypoint &&& %s' %  box
    query += ' and c.id = e.collection_id'
    query += ' and e.id = n.experiment_id'
    query += ' and l.id = n.layer_id'
    query += ' and c.name = %s' % collection_e
    query += ' and e.name = %s' % experiment_e
    query += ' and l.name = %s' % layer_e
    if id:
        query += " and n.name = '%s'" % id
    query += ';'
    return cls.objects.raw(query)

def get_filtered_ids(cls, collection, experiment, layer,
                     x_start, y_start, z_start, x_stop, y_stop, z_stop):
    '''
    Returns a list of ids for objects (neuron or synapse) in the given location.
    '''
    return [obj.name for obj in \
            filtered_query(cls, collection, experiment, layer,
                           x_start, y_start, z_start, x_stop, y_stop, z_stop)]

def get_filtered_object(cls, collection, experiment, layer,
                        x_start, y_start, z_start, x_stop, y_stop, z_stop, id):
    '''
    Returns a single object (neuron or synapse) in the given location with the given ID.
    Returns a Response object if an error occurs:
       Response with an http 400 error if no object is found.
       Response with a 500 error if more than one object with the same ID and location is found.
    '''
    objs = [obj for obj in \
            filtered_query(cls, collection, experiment, layer,
                         x_start, y_start, z_start, x_stop, y_stop, z_stop, id)]
    if len(objs)==0:
        err_msg = "Not found: %s with collection=%s, experiment=%s, layer=%s, id=%s" % \
                  (cls.__name__, collection, experiment, layer, id)
        return Response(err_msg, status.HTTP_400_BAD_REQUEST)
    if len(objs)>1:
        err_msg = "Not unique, found %s objects with collection=%s, experiment=%s, layer=%s, id=%s" % \
                  (len(objs), collection, experiment, layer, id)
        return Response(err_msg, status.HTTP_500_INTERNAL_SERVER_ERROR)
    return objs[0]


# S1
@api_view(['GET'])
def is_synapse(request, collection, experiment, layer, id):
    synapse = Synapse.get_obj_or_400(collection, experiment, layer, id)
    if isinstance(synapse, Synapse):
        found = True
    else:
        neuron = Neuron.get_obj_or_400(collection, experiment, layer, id)
        if isinstance(neuron, Neuron):
            found = False   # found a Neuron instead of a Synapse, so return false
        else:
            return synapse  # return HTTP_400 response
    result = { "result": found }
    return Response(result, status=status.HTTP_200_OK)

# S2
@api_view(['GET'])
def synapse_ids(request, collection, experiment, layer, resolution,
                           x_start, x_stop, y_start, y_stop, z_start, z_stop):
    ids = get_filtered_ids(Synapse, collection, experiment, layer,
                           x_start, y_start, z_start, x_stop, y_stop, z_stop)
    result = { "ids": ids }
    return Response(result, status=status.HTTP_200_OK)

# S3 
@api_view(['GET'])
def synapse_keypoint(request, collection, experiment, layer, resolution, id):
    synapse = Synapse.get_obj_or_400(collection, experiment, layer, id)
    if isinstance(synapse, Response):
        return synapse  # return HTTP_400 response
    result = { "keypoint": synapse.keypoint.coords }
    return Response(result, status=status.HTTP_200_OK)

# S4
@api_view(['GET'])
def synapse_parent(request, collection, experiment, layer, id):
    synapse = Synapse.get_obj_or_400(collection, experiment, layer, id)
    if isinstance(synapse, Response):
        return synapse  # return HTTP_400 response
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


# S5
@api_view(['GET'])
def is_neuron(request, collection, experiment, layer, id):
    neuron = Neuron.get_obj_or_400(collection, experiment, layer, id)
    if isinstance(neuron, Neuron):
        found = True
    else:
        synapse = Synapse.get_obj_or_400(collection, experiment, layer, id)
        if isinstance(synapse, Synapse):
            found = False   # found a Synapse instead of a Neuron, so return false
        else:
            return neuron  # return HTTP_400 response
    result = { "result": found }
    return Response(result, status=status.HTTP_200_OK)

# S6
@api_view(['GET'])
def neuron_ids(request, collection, experiment, layer, resolution,
                           x_start, x_stop, y_start, y_stop, z_start, z_stop):
    ids = get_filtered_ids(Neuron, collection, experiment, layer,
                           x_start, y_start, z_start, x_stop, y_stop, z_stop)
    result = { "ids": ids }
    return Response(result, status=status.HTTP_200_OK)

# S7
@api_view(['GET'])
def neuron_keypoint(request, collection, experiment, layer, resolution, id):
    neuron = Neuron.get_obj_or_400(collection, experiment, layer, id)
    if isinstance(neuron, Response):
        return neuron  # return HTTP_400 response
    result = { "keypoint": neuron.keypoint.coords }
    return Response(result, status=status.HTTP_200_OK)

# S8
@api_view(['GET'])
def neuron_children(request, collection, experiment, layer,  resolution,
                        x_start, x_stop, y_start, y_stop, z_start, z_stop, id):
    neuron = get_filtered_object(Neuron, collection, experiment, layer,
                                 x_start, y_start, z_start, x_stop, y_stop, z_stop, id=id)
    if isinstance(neuron, Response):
        return neuron
    result = { "child_synapses": dict([(s.name, s.polarity) for s in neuron.synapses.all() ]) }
    return Response(result, status=status.HTTP_200_OK)

# S9
@api_view(['GET'])
def voxel_list(request, collection, experiment, layer,  resolution,
                     x_start, x_stop, y_start, y_stop, z_start, z_stop, id):
    neuron = get_filtered_object(Neuron, collection, experiment, layer,
                                 x_start, y_start, z_start, x_stop, y_stop, z_stop, id=id)
    if isinstance(neuron, Response):
        return neuron    
    coords = [coord for coord in zip(*neuron.geometry)]
    result = { "x": coords[0],
               "y": coords[1],
               "z": coords[2] }
    return Response(result, status=status.HTTP_200_OK)


# S9 - proxy call to theboss.io
@api_view(['GET'])
def voxel_list_remote(request, collection, experiment, layer,  resolution,
               x_start, x_stop,
               y_start, y_stop,
               z_start, z_stop, id):
    # Proxy call to theboss.io
    boss = BossClient()
    # Dummy placeholder - Need voxels instead
    result = boss.get_layer(layer, collection, experiment)
    return Response(result.raw, status=status.HTTP_200_OK)


# S10
@api_view(['GET'])
def synapse_compartment(request, collection, experiment, layer,  id):
    synapse = Synapse.get_obj_or_400(collection, experiment, layer, id)
    if isinstance(synapse, Response):
        return synapse  # return HTTP_400 response
    result = { "compartment": Compartment(synapse.compartment).name }
    return Response(result, status=status.HTTP_200_OK)

# S11
@api_view(['GET'])
def neuron_celltype(request, collection, experiment, layer,  id):
    neuron= Neuron.get_obj_or_400(collection, experiment, layer, id)
    if isinstance(neuron, Response):
        return neuron  # return HTTP_400 response
    result = { "cell_type": CellType(neuron.cell_type).name }
    return Response(result, status=status.HTTP_200_OK)

# S12
@api_view(['GET'])
def neuron_stimulus(request, collection, experiment, layer,  id, start_time, end_time):
    neuron = Neuron.get_obj_or_400(collection, experiment, layer, id)
    if isinstance(neuron, Response):
        return neuron  # return HTTP_400 response
    series = NeuronStimulus.get_by_time(neuron.experiment, neuron, start_time, end_time)
    if len(series) == 0:
        err_msg = "No values found for (%s <= time < %s) on neuron %s " % \
                  (start_time, end_time, id)
        return Response(err_msg, status.HTTP_400_BAD_REQUEST)
    result = { "stimulus": [(ns.time, ns.value) for ns in series] }
    return Response(result, status=status.HTTP_200_OK)

# S13
@api_view(['GET'])
def neuron_activity(request, collection, experiment, layer, id, start_time, end_time):
    neuron = Neuron.get_obj_or_400(collection, experiment, layer, id)
    if isinstance(neuron, Response):
        return neuron  # return HTTP_400 response
    series = NeuronActivity.get_by_time(neuron.experiment, neuron, start_time, end_time)
    if len(series) == 0:
        err_msg = "No values found for (%s <= time < %s) on neuron %s " % \
                  (start_time, end_time, id)
        return Response(err_msg, status.HTTP_400_BAD_REQUEST)
    result = { "activity": [(na.time, na.value) for na in series] }
    return Response(result, status=status.HTTP_200_OK)
