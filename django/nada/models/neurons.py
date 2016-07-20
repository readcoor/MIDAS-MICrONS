from django.db import models
from .util import NameLookupMixin, ChoiceEnum
from .samples import Experiment, Layer
from django.contrib.gis.db import models as gis_models
from django.shortcuts import get_object_or_404

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

class CELIMixin:
    """
    Looks up an object (neuron or synapse) matching the given collection/experiment/layer/id
    Returns None if none found.
    """
    
    @classmethod
    def get_by_celi(cls, collection_name, experiment_name, layer_name, id):
        return cls.objects \
               .filter(experiment__collection__name=collection_name) \
               .filter(experiment__name=experiment_name) \
               .filter(layer__name=layer_name) \
               .filter(name=id) \
               .first()

class Neuron(NameLookupMixin, CELIMixin, models.Model):
    """
    Object representing a Neuron
    """
    name = models.BigIntegerField(unique=True)
    experiment = models.ForeignKey(Experiment, related_name='neurons', on_delete=models.PROTECT) # Parent
    layer = models.ForeignKey(Layer, related_name='neurons', on_delete=models.PROTECT) # Parent
    cell_type = models.CharField(max_length=1, choices=CellType.choices())
    geometry = gis_models.MultiPointField(dim=3) # [Point(x,y,z)...]
    keypoint = gis_models.PointField(dim=3) # Point(x,y,z)
    # activity - TBD

    # a = nada.models.Neuron.get_by_name(444)
    # b = nada.models.Neuron.get_by_celi('collection1', 'experiment1', 'layer1', 444)

class Synapse(NameLookupMixin, CELIMixin, models.Model):
    """
    Object representing a Synapse
    """
    name = models.BigIntegerField(unique=True)
    experiment = models.ForeignKey(Experiment, related_name='synapses', on_delete=models.PROTECT) # Parent
    layer = models.ForeignKey(Layer, related_name='synapses', on_delete=models.PROTECT) # Parent
    neuron = models.ForeignKey(Neuron, related_name='synapses', on_delete=models.PROTECT)
    partner_neuron = models.ForeignKey(Neuron, related_name='partner_synapses', on_delete=models.PROTECT)
    partner_synapse = models.OneToOneField('self',
                                           related_name='+',  # Use partner_synapse for both partners.
                                                              # No backwards relation
                                           on_delete=models.PROTECT)
    geometry = gis_models.MultiPointField(dim=3)   # [ GISPoint(x,y,z), ... ]
    keypoint = gis_models.PointField(dim=3)        # GISPoint(x,y,z)
    polarity = models.CharField(max_length=1, choices=Polarity.choices())
    compartment = models.FloatField()

