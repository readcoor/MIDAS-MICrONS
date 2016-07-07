import yaml
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from models import *

def add_yaml(string, obj):
    return '%s\n---\n%s' % (string, yaml.dump(obj))
    #return string

# POST /collection/
class CollectionPostViewSet(viewsets.ModelViewSet):
    '''Create a new collection'''
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

# GET /collections/
class CollectionsViewSet(viewsets.ModelViewSet):
    '''List all collections'''
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

# [GET,PUT,DELETE] /collection/:name/
class CollectionViewSet(viewsets.ModelViewSet):
    '''Get a collection's details'''
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    lookup_field = 'name'
    docstrings = [('retrieve', 'Retrieve a collection'),
                  ('update', add_yaml('Update a collection', 
                                      {'parameters':[{'name':'name','paramType':'path'}]})),
                  ('destroy', 'Delete a collection')]



# POST /coordinateframe/
class CoordinateFramePostViewSet(viewsets.ModelViewSet):
    '''Create a new coordinateframe'''
    queryset = CoordinateFrame.objects.all()
    serializer_class = CoordinateFrameSerializer

# GET /coordinateframes/
class CoordinateFramesViewSet(viewsets.ModelViewSet):
    '''List all coordinateframes'''
    queryset = CoordinateFrame.objects.all()
    serializer_class = CoordinateFrameSerializer

# [GET,PUT,DELETE] /coordinateframe/:name/
class CoordinateFrameViewSet(viewsets.ModelViewSet):
    '''Get a coordinateframe's details'''
    queryset = CoordinateFrame.objects.all()
    serializer_class = CoordinateFrameSerializer
    lookup_field = 'name'
    docstrings = [('retrieve', 'Retrieve a coordinateframe'),
                  ('update', add_yaml('Update a coordinateframe', 
                                      {'parameters':[{'name':'name','paramType':'path'}]})),
                  ('destroy', 'Delete a coordinateframe')]


# POST /experiment/
class ExperimentPostViewSet(viewsets.ModelViewSet):
    '''Create a new experiment'''
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

# GET /coordinateframes/
class ExperimentsViewSet(viewsets.ModelViewSet):
    '''List all experiments'''
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

# [GET,PUT,DELETE] /experiment/:collection/:name/
class ExperimentViewSet(viewsets.ModelViewSet):
    '''Get an experiment's details'''
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    lookup_field = ['name']
    #multiple_lookup_fields = ['collection', 'name']
    docstrings = [('retrieve', 'Retrieve an experiment'),
                  ('update', add_yaml('Update an experiment', 
                                      {'parameters':[{'name':'name','paramType':'path'}]})),
                  ('destroy', 'Delete an experiment')]

    
    def get_object(self):
        col_name = self.kwargs['collection']
        exp_name = self.kwargs['name']
        objects = self.get_queryset().filter(collection__name=col_name).filter(name=exp_name)
        obj = get_object_or_404(objects)
        self.check_object_permissions(self.request, obj)
        return obj

def init_docstrings(cls):
    for (fcn, string) in cls.docstrings:
        getattr(cls, fcn).__func__.__doc__ = string


# POST /layer/
class LayerPostViewSet(viewsets.ModelViewSet):
    '''Create a new layer'''
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer

# GET /layer/
class LayersViewSet(viewsets.ModelViewSet):
    '''List all layers'''
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer

# [GET,PUT,DELETE] /layer/:collection/:experiment/:name/
class LayerViewSet(viewsets.ModelViewSet):
    '''Get an layer's details'''
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    lookup_field = ['name']
    #multiple_lookup_fields = ['collection', 'name']
    docstrings = [('retrieve', 'Retrieve a layer'),
                  ('update', add_yaml('Update a layer', 
                                      {'parameters':[{'name':'name','paramType':'path'}]})),
                  ('destroy', 'Delete a layer')]
    
    def get_object(self):
        col_name = self.kwargs['collection']
        exp_name = self.kwargs['experiment']
        layer_name = self.kwargs['name']
        objects = self.get_queryset().filter(experiment__collection__name=col_name).filter(experiment__name=exp_name).filter(name=layer_name)
        obj = get_object_or_404(objects)
        self.check_object_permissions(self.request, obj)
        return obj


init_docstrings(CollectionViewSet)
init_docstrings(CoordinateFrameViewSet)
init_docstrings(ExperimentViewSet)
init_docstrings(LayerViewSet)
