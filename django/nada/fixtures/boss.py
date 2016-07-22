from ..models import Layer, Experiment, CoordinateFrame, Collection

BOSS_CLASSES = [Layer, Experiment, CoordinateFrame, Collection]

def boss_setup():
    '''Sets up some sample objects for testing and debugging'''
    collection1 = Collection(name='collection1')
    collection1.save()
    coord_params = {'x_start':0, 'x_stop':1000,
                    'y_start':0, 'y_stop':1000,
                    'z_start':0, 'z_stop':1000,
                    'x_voxel_size': 1.0, 'y_voxel_size': 1.0, 'z_voxel_size': 1.0, 
                    'voxel_unit': 'NANOMETERS',
                    'time_step': 1,
                    'time_step_unit': 'SECONDS'}
    coord1 = CoordinateFrame(name='coord1', **coord_params)
    coord1.save()
    experiment1 = Experiment(name='experiment1', collection=collection1, coord_frame=coord1)
    experiment1.save()
    experiment2 = Experiment(name='experiment2', collection=collection1, coord_frame=coord1)
    experiment2.save()
    layer_params = {'default_time_step':0, 'base_resolution':0, 'datatype':'uint64'}
    layer1 = Layer(name='layer1', experiment=experiment1, is_channel=False, **layer_params)
    layer2 = Layer(name='layer2', experiment=experiment1, is_channel=False, **layer_params)
    layer3 = Layer(name='layer3', experiment=experiment1, is_channel=False, **layer_params)
    layer4 = Layer(name='layer4', experiment=experiment2, is_channel=False, **layer_params)
    layer5 = Layer(name='layer5', experiment=experiment2, is_channel=False, **layer_params)
    layer6 = Layer(name='layer6', experiment=experiment2, is_channel=False, **layer_params)
    channelA = Layer(name='channelA', experiment=experiment1, is_channel=True, **layer_params)
    channelB = Layer(name='channelB', experiment=experiment1, is_channel=True, **layer_params)
    channelC = Layer(name='channelC', experiment=experiment2, is_channel=True, **layer_params)
    channelD = Layer(name='channelD', experiment=experiment2, is_channel=True, **layer_params)
    for obj in [layer1, layer2, layer3, layer4, layer5, layer6,
                channelA, channelB, channelC, channelD]:
        obj.save()

