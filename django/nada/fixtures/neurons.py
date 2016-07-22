import random
from . import boss
from ..models import Neuron, Synapse, Layer
from django.contrib.gis.geos import Point, MultiPoint

NEURONS_CLASSES = [Neuron, Synapse]

# nada.fixtures.utils.nuke_all(nada.fixtures.NEURONS_CLASSES)
# nada.fixtures.utils.is_empty(nada.fixtures.NEURONS_CLASSES)
# nada.fixtures.neurons.setup(**nada.fixtures.NEURONS_TEST_OPTIONS)

# Set up 500 neurons, with about 500 voxels each.

NEURONS_DEFAULT_OPTIONS = { 'N_NEURONS' : 500,
                            'POINTS_PER_NEURON' : 500,
                            'N_SYNAPSES' : 1000,
                            'POINTS_PER_SYNAPSE' : 50
                            }

NEURONS_TEST_OPTIONS = { 'N_NEURONS' : 50,
                         'POINTS_PER_NEURON' : 50,
                         'N_SYNAPSES' : 100,
                         'POINTS_PER_SYNAPSE' : 5
                         }

def neurons_setup(**options):
    '''Sets up some sample objects for testing and debugging'''
    layer1 = Layer.get_by_name('layer1')
    experiment1 = layer1.experiment

    neurons = []
    synapses = []

    for neuron_id in range(0, options['N_NEURONS']):
        neuron = Neuron(name=neuron_id, layer=layer1, experiment=experiment1)
        neurons.append(neuron)
        center_y = random.randrange(2000)
        center_z = random.randrange(2000)
        pts = [Point(neuron_id + random.randrange(-100, 100), 
                     center_y + random.randrange(-100, 100), 
                     center_z + random.randrange(-100, 100)) \
               for p in range(0, options['POINTS_PER_NEURON'])]
        neuron.geometry = MultiPoint(pts)
        neuron.keypoint = Point(neuron_id, center_y, center_z) # neuron.geometry.centroid is 2D
        neuron.save()

    assert(len(neurons) == options['N_NEURONS'])
    for synapse_id in range(0, options['N_SYNAPSES']):
        random_neuron = neurons[random.randrange(0, options['N_NEURONS'])]
        synapse = Synapse(name=synapse_id,
                          layer=layer1,
                          experiment=experiment1,
                          neuron=random_neuron,
                          compartment=random.random())
        synapses.append(synapse)
        center_y = random.randrange(2000)
        center_z = random.randrange(2000)
        pts = [Point(synapse_id + random.randrange(-100, 100), 
                     center_y + random.randrange(-100, 100), 
                     center_z + random.randrange(-100, 100)) \
               for p in range(0, options['POINTS_PER_SYNAPSE'])]
        synapse.geometry = MultiPoint(pts)
        synapse.keypoint = Point(synapse_id, center_y, center_z) # synapse.geometry.centroid is 2D
    for synapse in synapses:
        if synapse.partner_synapse == None:
            partner = random_other(synapse, synapses)
            synapse.save()
            partner.save()
            synapse.partner_synapse = partner
            synapse.partner_neuron = partner.neuron
            partner.partner_synapse = synapse
            partner.partner_neuron = synapse.neuron
            synapse.save()
            partner.save()
            synapses.remove(synapse)
            synapses.remove(partner)

def random_other(item, list):
    'Returns an element of list which is not item'
    other = item
    while other == item:
        other = random.choice(list)
    return other
