# Copyright 2016 Wyss Institute
# portions Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models
from . import validators


__all__ = ['Collection', 'Experiment', 'CoordinateFrame', 'Layer']

class NameLookupModel(models.Model):
    @classmethod
    def get_by_name(cls, name):
        '''
        Raises:
          MultipleObjectsReturned: If more than one object found with given name
          cls.DoesNotExist:        If no object found
        '''
        return cls.objects.filter(name=name).get()

    class Meta:
        abstract = True


class Collection(NameLookupModel):
    """
    Object representing a Boss Collection
    """
    name = models.CharField(max_length=255, verbose_name="Name of the Collection",
                            validators=[validators.NameValidator()], unique=True)
    description = models.CharField(max_length=4096, blank=True)

    def __str__(self):
        return self.name


class Experiment(NameLookupModel):
    """
    Object representing a BOSS experiment
    """
    collection = models.ForeignKey(Collection, related_name='experiments', on_delete=models.PROTECT) # Parent
    name = models.CharField(max_length=255, verbose_name="Name of the Experiment", validators=[validators.NameValidator()])
    description = models.CharField(max_length=4096, blank=True)

    coord_frame = models.ForeignKey('CoordinateFrame', related_name='coord', on_delete=models.PROTECT)
    num_hierarchy_levels = models.IntegerField(default=0)

    HIERARCHY_METHOD_CHOICES = (
        ('near_iso', 'NEAR_ISO'),
        ('iso', 'ISO'),
        ('slice', 'SLICE'),
    )
    hierarchy_method = models.CharField(choices=HIERARCHY_METHOD_CHOICES, max_length=100)
    max_time_sample = models.IntegerField(default=0)

    class Meta:
        unique_together = ('collection', 'name')

    def __str__(self):
        return self.name


class CoordinateFrame(NameLookupModel):
    """
    Coordinate Frame for Boss Experiments

    """
    name = models.CharField(max_length=255, verbose_name="Name of the Coordinate reference frame",
                            validators=[validators.NameValidator()], unique=True)
    description = models.CharField(max_length=4096, blank=True)

    x_start = models.IntegerField()
    x_stop = models.IntegerField()
    y_start = models.IntegerField()
    y_stop = models.IntegerField()
    z_start = models.IntegerField()
    z_stop = models.IntegerField()

    x_voxel_size = models.FloatField()
    y_voxel_size = models.FloatField()
    z_voxel_size = models.FloatField()

    VOXEL_UNIT_CHOICES = (
        ('nanometers', 'NANOMETERS'),
        ('micrometers', 'MICROMETERS'),
        ('millimeters', 'MILLIMETERS'),
        ('centimeters', 'CENTIMETERS')
    )
    voxel_unit = models.CharField(choices=VOXEL_UNIT_CHOICES, max_length=100)
    time_step = models.IntegerField()
    TIMESTEP_UNIT_CHOICES = (
        ('nanoseconds', 'NANOSECONDS'),
        ('microseconds', 'MICROSECONDS'),
        ('milliseconds', 'MILLISECONDS'),
        ('seconds', 'SECONDS'),
    )
    time_step_unit = models.CharField(choices=TIMESTEP_UNIT_CHOICES, max_length=100)

    def __str__(self):
        return self.name



class Layer(NameLookupModel):
    """
    Object representing a channel or layer. For image datasets these are channels and for annotations datasets these
    are layers.
    """
    name = models.CharField(max_length=255, verbose_name="Name of the Layer", validators=[validators.NameValidator()])
    description = models.CharField(max_length=4096, blank=True)

    experiment = models.ForeignKey(Experiment, related_name='layers', on_delete=models.PROTECT)
    is_channel = models.BooleanField()
    base_resolution = models.IntegerField(default=0)
    default_time_step = models.IntegerField(default=0)
    DATATYPE_CHOICES = (
        ('uint8', 'UINT8'),
        ('uint16', 'UINT16'),
        ('uint32', 'UINT32'),
        ('uint64', 'UINT64'),
    )

    datatype = models.CharField(choices=DATATYPE_CHOICES, max_length=100)

    class Meta:
        unique_together = ('experiment', 'name')

    def __str__(self):
        return self.name

