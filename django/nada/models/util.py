from django.db import models
import inspect
from enum import IntEnum

class NameLookupMixin:
    @classmethod
    def get_by_name(cls, name):
        '''
        Raises:
          MultipleObjectsReturned: If more than one object found with given name
          cls.DoesNotExist:        If no object found
        '''
        return cls.objects.filter(name=name).get()

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)


class ChoiceEnum(IntEnum):
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
    
