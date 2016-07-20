from django.db import models
from .util import NameLookupModel, ChoiceEnum
from .samples import Experiment
from django.contrib.gis.db import models as gis_models

__all__ = ['Neuron', 'Synapse']

class Polarity(ChoiceEnum):
    "Allowed synapse polarity values (Enum)"
    unknown = 0
    pre = 1
    post = 2
    bidirectional = 3

# PLACEHOLDER VALUES
class CellType(ChoiceEnum):
    "Allowed cell type values (Enum)"
    unknown = 0
    red = 1
    green = 2
    blue = 3

class Neuron(NameLookupModel):
    """
    Object representing a Neuron
    """
    name = models.BigIntegerField(unique=True)
    experiment = models.ForeignKey(Experiment, related_name='neurons', on_delete=models.PROTECT) # Parent
    cell_type = models.CharField(max_length=1, choices=CellType.choices())
    geometry = gis_models.MultiPointField() # [GISPoint(x,y,z)...]
    keypoint = gis_models.PointField() # GISPoint(x,y,z)

    # activity - TBD


class Synapse(NameLookupModel):
    """
    Object representing a Synapse
    """
    name = models.BigIntegerField(unique=True)
    experiment = models.ForeignKey(Experiment, related_name='synapses', on_delete=models.PROTECT) # Parent
    neuron = models.ForeignKey(Neuron, related_name='synapses', on_delete=models.PROTECT)
    partner_neuron = models.ForeignKey(Neuron, related_name='partner_synapses', on_delete=models.PROTECT)
    partner_synapse = models.OneToOneField('self',
                                           related_name='+',  # Use partner_synapse for both partners.
                                                              # No backwards relation
                                           on_delete=models.PROTECT)
    geometry = gis_models.MultiPointField()   # [ GISPoint(x,y,z), ... ]
    keypoint = gis_models.PointField()        # GISPoint(x,y,z)
    polarity = models.CharField(max_length=1, choices=Polarity.choices())
    compartment = models.FloatField()
    
