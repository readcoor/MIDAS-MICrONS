from django.db import models
from .util import NameLookupMixin, ChoiceEnum
from .samples import Experiment, Layer
from django.contrib.gis.db import models as gis_models
from rest_framework.response import Response
from rest_framework import status


__all__ = ['Neuron', 'Synapse', 'Polarity', 'CellType', 'Compartment',
           'NeuronStimulus', 'NeuronActivity']

class Polarity(ChoiceEnum):
    "Allowed synapse polarity values (Enum)"
    unknown = 0
    pre = 1
    post = 2
    bidirectional = 3

class CellType(ChoiceEnum):
    "Allowed cell type values (Enum)"
    unknown = 0
    excitatory = 1
    inhibitory = 2

class Compartment(ChoiceEnum):
    "Allowed synapse compartment values (Enum)"
    unknown = 0
    soma = 1
    proximal = 2
    distal = 3
    apical = 4
    axon = 5

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

    @classmethod
    def get_obj_or_400(cls, collection_name, experiment_name, layer_name, id):
        '''
        If obj is None, Raise HTTP 400 Bad Request error
        Similar to django.shortcuts.get_object_or_404
        '''
        obj = cls.get_by_celi(collection_name, experiment_name, layer_name, id)
        if obj is None:
            err_msg = "Not found: %s with collection=%s, experiment=%s, layer=%s, id=%s" % \
                      (cls.__name__, collection_name, experiment_name, layer_name, id)
            return Response(err_msg, status.HTTP_400_BAD_REQUEST)
        return obj

class TimeSeriesMixin:
    """
    Looks up time-series data for the given neuron within the given time interval.
    Returns samples in ascending time order.
    Returns None if none found.
    """
    @classmethod
    def get_by_time(cls, experiment, neuron, start_time, end_time):
        return cls.objects \
               .filter(experiment=experiment) \
               .filter(neuron=neuron) \
               .filter(time__gte=start_time) \
               .filter(time__lt=end_time) \
               .order_by('time') \
               .all()

    @classmethod
    def get_one(cls, experiment, neuron, time):
        return cls.objects \
               .filter(experiment=experiment) \
               .filter(neuron=neuron) \
               .filter(time=time) \
               .get()

class Neuron(models.Model):
    """
    Object representing a Neuron
    """
    name = models.BigIntegerField(unique=True)
    experiment = models.ForeignKey(Experiment, related_name='neurons', on_delete=models.PROTECT) # Parent
    layer = models.ForeignKey(Layer, related_name='neurons', on_delete=models.PROTECT) # Parent
    cell_type = models.IntegerField(choices=CellType.choices(), default=CellType.unknown.value)
    geometry = gis_models.MultiPointField(dim=3, srid=0, spatial_index=False) # [Point(x,y,z)...]
    keypoint = gis_models.PointField(dim=3, srid=0, spatial_index=False) # Point(x,y,z)

class Mesh3D_FullTile(models.Model):
    """
    A mesh of tile sized (2560, 2160, 50) rectangles
    """
    box = gis_models.MultiPointField(dim=3, srid=0, spatial_index=False)


class Neuron_To_Mesh(NameLookupMixin, CELIMixin, models.Model):
    """
    Join table that links Neurons to the Mesh table for optimizing queries
    """
    experiment = models.ForeignKey(Experiment, related_name='neuron_to_mesh', on_delete=models.CASCADE)
    neuron = models.ForeignKey(Neuron, related_name='neuron_to_mesh', on_delete=models.CASCADE)    
    mesh3d_fulltile = models.ForeignKey(Mesh3D_FullTile, related_name='neuron_to_mesh')


class Synapse(NameLookupMixin, CELIMixin, models.Model):
    """
    Object representing a Synapse
    """
    name = models.BigIntegerField(unique=True)
    experiment = models.ForeignKey(Experiment, related_name='synapses', on_delete=models.PROTECT) # Parent
    layer = models.ForeignKey(Layer, related_name='synapses', on_delete=models.PROTECT) # Parent
    neuron = models.ForeignKey(Neuron, related_name='synapses', on_delete=models.CASCADE,
                               blank=True, null=True)
    partner_neuron = models.ForeignKey(Neuron, related_name='partner_synapses', on_delete=models.CASCADE,
                                       blank=True, null=True)
    partner_synapse = models.OneToOneField('self',
                                           blank=True, null=True,
                                           related_name='+',  # Use partner_synapse for both partners.
                                                              # No backwards relation
                                           on_delete=models.CASCADE)
    geometry = gis_models.MultiPointField(dim=3, srid=0, spatial_index=False)   # [ GISPoint(x,y,z), ... ]
    keypoint = gis_models.PointField(dim=3, srid=0, spatial_index=False)        # GISPoint(x,y,z)
    polarity = models.IntegerField(choices=Polarity.choices(), default=Polarity.unknown.value)
    compartment = models.FloatField()

class NeuronStimulus(TimeSeriesMixin, models.Model):
    neuron = models.ForeignKey(Neuron, related_name='stimulus', on_delete=models.CASCADE,
                               blank=False, null=False)
    experiment = models.ForeignKey(Experiment, related_name='+', on_delete=models.CASCADE,
                               blank=False, null=False)
    time = models.IntegerField(blank=False, null=False)
    value = models.IntegerField(blank=False, null=False)
    
    class Meta:
        unique_together = (('neuron', 'experiment', 'time'),)

class NeuronActivity(TimeSeriesMixin, models.Model):
    neuron = models.ForeignKey(Neuron, related_name='activity', on_delete=models.CASCADE,
                               blank=False, null=False)
    experiment = models.ForeignKey(Experiment, related_name='+', on_delete=models.CASCADE,
                               blank=False, null=False)
    time = models.IntegerField(blank=False, null=False)
    value = models.FloatField(blank=False, null=False)
    
    class Meta:
        unique_together = (('neuron', 'experiment', 'time'),)
