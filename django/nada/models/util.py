from django.db import models
import inspect
from enum import Enum

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


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices
    
