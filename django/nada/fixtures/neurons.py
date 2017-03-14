import random
from . import boss
from ..models import Neuron, Synapse, Channel, Polarity, CellType, Compartment, \
     NeuronStimulus, NeuronActivity
from django.contrib.gis.geos import Point, MultiPoint

NEURONS_CLASSES = [Neuron, Synapse]

# nada.fixtures.utils.nuke_all(nada.fixtures.NEURONS_CLASSES)
# nada.fixtures.utils.nuke_all(nada.fixtures.BOSS_CLASSES)
#
# nada.fixtures.utils.is_empty(nada.fixtures.NEURONS_CLASSES)
#
# nada.fixtures.boss_setup()
# nada.fixtures.neurons_setup(**nada.fixtures.NEURONS_TEST_OPTIONS)
# nada.fixtures.neurons_setup(**nada.fixtures.NEURONS_DEFAULT_OPTIONS)

# Set up 500 neurons, with about 500 voxels each.

NEURONS_DEFAULT_OPTIONS = { 'N_NEURONS' : 500,
                            'POINTS_PER_NEURON' : 500,
                            'N_SYNAPSES' : 1000,
                            'POINTS_PER_SYNAPSE' : 50,
                            'N_STIMULUS_ENTRIES' : 100,
                            'N_ACTIVITY_ENTRIES' : 100,
                            }

NEURONS_TEST_OPTIONS = { 'N_NEURONS' : 50,
                         'POINTS_PER_NEURON' : 50,
                         'N_SYNAPSES' : 100,
                         'POINTS_PER_SYNAPSE' : 5,
                         'N_STIMULUS_ENTRIES' : 10,
                         'N_ACTIVITY_ENTRIES' : 10,
                         }

def neurons_setup(**options):
    '''Sets up some sample objects for testing and debugging'''
    channel1 = Channel.get_by_name('channel1')  # neurons
    channel2 = Channel.get_by_name('channel2')  # synapses
    experiment1 = channel1.experiment
    neurons = []
    synapses = []

    for neuron_id in range(0, options['N_NEURONS']):
        neuron = Neuron(name=neuron_id, channel=channel1, experiment=experiment1)
        neurons.append(neuron)
        center_y = random.randrange(2000)
        center_z = random.randrange(2000)
        pts = [Point(neuron_id + random.randrange(-100, 100), 
                     center_y + random.randrange(-100, 100), 
                     center_z + random.randrange(-100, 100)) \
               for p in range(0, options['POINTS_PER_NEURON'])]
        neuron.geometry = MultiPoint(pts)
        neuron.keypoint = Point(neuron_id, center_y, center_z) # neuron.geometry.centroid is 2D
        if neuron_id > 0:
            if (neuron_id % 2 == 0):    # odd or even (0 == 'unknown')
                neuron.cell_type = CellType.excitatory
            else:
                neuron.cell_type = CellType.inhibitory
        neuron.save()
        define_stimulus_and_activity(neuron, options)

    assert(len(neurons) == options['N_NEURONS'])
    for synapse_id in range(0, options['N_SYNAPSES']):
        synapse = create_synapse(synapse_id, neurons, \
                                 channel=channel2, experiment=experiment1, options=options)
        synapses.append(synapse)
    assert(len(synapses) == options['N_SYNAPSES'])        
    match_synapses(synapses)
        
def match_synapses(synapses):
    '''
    Assign pairs of synapses to each other
    '''
    while len(synapses)>0:
        synapse = synapses[0]
        if synapse.partner_synapse == None:
            partner = choose_partner(synapse, synapses)
            if random.randint(0, 1) == 0:
                synapse.polarity = Polarity.pre.value
                partner.polarity = Polarity.post.value
            else:
                synapse.polarity = Polarity.post.value
                partner.polarity = Polarity.pre.value
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

def create_synapse(synapse_id, neurons, channel, experiment, options):
    random_neuron = neurons[random.randrange(0, options['N_NEURONS'])]
    synapse = Synapse(name=synapse_id,
                      channel=channel,
                      experiment=experiment,
                      neuron=random_neuron,
                      compartment=random.random())
    center_y = random.randrange(2000)
    center_z = random.randrange(2000)
    pts = [Point(synapse_id + random.randrange(-100, 100), 
                 center_y + random.randrange(-100, 100), 
                 center_z + random.randrange(-100, 100)) \
           for p in range(0, options['POINTS_PER_SYNAPSE'])]
    synapse.geometry = MultiPoint(pts)
    synapse.keypoint = Point(synapse_id, center_y, center_z) # synapse.geometry.centroid is 2D
    max_compartment_value = (Compartment.axon.value + 1) # axon == 5
    synapse.compartment = Compartment(synapse_id % max_compartment_value) # assign value between 0-5
    return synapse

def define_stimulus_and_activity(neuron, options):
    exp = neuron.experiment
    for time in range(0,options['N_STIMULUS_ENTRIES']):
        value = random.randrange(-10, 10)
        s = NeuronStimulus(neuron=neuron, experiment=exp, time=time, value=value)
        s.save()
    for time in range(0,options['N_ACTIVITY_ENTRIES']):
        value = random.random()
        a = NeuronActivity(neuron=neuron, experiment=exp, time=time, value=value)
        a.save()
        #print('**a', a, neuron.name, exp, time, value)

def choose_partner(synapse, others):
    '''
    Returns a partner (another synapse) for a synapse.
    Others = a list of available unassigned synapses.
    Guarantees that synapse and the partner do not both belong to the same neuron.
    '''
    options = others.copy()
    while len(options)>1 or (len(options)==1 and synapse != options[0]):
        # while there are still valid options
        choice = random_other(synapse, options)
        if choice.neuron == synapse.neuron:
            # don't choose another synapse on the same neuron
            options.remove(choice)
        else:
            return choice
    # all other synapses have the same neuron, so pick a free synapse and change its neuron
    choice = random_other(synapse, others)
    neuron_id = synapse.neuron.name
    # reassign the chosen synapse's neuron
    other_neurons = [n for n in Neuron.objects.exclude(name=neuron_id)]
    choice.neuron = random.choice(other_neurons)
    return choice

def random_other(item, list):
    '''
    Returns an element of list which is not item
    Throws an exception if list has no valid alternatives.
    '''
    if len(list) == 0 or (len(list)==1 and item == list[0]):
        raise Exception('No alternatives to choose from')
    other = item
    while other == item:
        other = random.choice(list)
    return other
