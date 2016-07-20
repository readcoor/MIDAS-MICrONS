from . import boss
from ..models import Neuron, Synapse, Experiment


def setup():
    '''Sets up some sample objects for testing and debugging'''
    collection1 = Collection(name='collection1')
    collection1.save()
    
