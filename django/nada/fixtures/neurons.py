import random
from . import boss
from ..models import Neuron, Synapse, Layer
from django.contrib.gis.geos import Point, MultiPoint

CLASSES = [Neuron]

# nada.fixtures.utils.nuke_all(nada.fixtures.neurons.CLASSES)
# nada.fixtures.utils.is_empty(nada.fixtures.neurons.CLASSES)
# nada.fixtures.neurons.setup()

# Set up 500 neurons, with about 500 voxels each.

def setup():
    '''Sets up some sample objects for testing and debugging'''
    layer1 = Layer.get_by_name('layer1')
    experiment1 = layer1.experiment
    N_NEURONS = 500
    POINTS_PER_NEURON = 500

    for neuron_id in range(0, N_NEURONS):
        neuron = Neuron(name=neuron_id, layer=layer1, experiment=experiment1)
        center_y = random.randrange(2000)
        center_z = random.randrange(2000)
        pts = [Point(neuron_id + random.randrange(-100, 100), 
                     center_y + random.randrange(-100, 100), 
                     center_z + random.randrange(-100, 100)) \
               for p in range(0, POINTS_PER_NEURON)]
        neuron.geometry = MultiPoint(pts)
        neuron.keypoint = Point(neuron_id, center_y, center_z) # neuron.geometry.centroid is 2D
        neuron.save()

    
