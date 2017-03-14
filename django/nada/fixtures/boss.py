from ..models import Channel, Experiment, CoordinateFrame, Collection

BOSS_CLASSES = [Channel, Experiment, CoordinateFrame, Collection]

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
    channel_params = {'default_time_step':0, 'base_resolution':0, 'datatype':'uint64'}
    channel1 = Channel(name='channel1', experiment=experiment1, is_channel=False, description="Neurons channel",  **channel_params)
    channel2 = Channel(name='channel2', experiment=experiment1, is_channel=False, description="Synapses channel", **channel_params)
    channel3 = Channel(name='channel3', experiment=experiment1, is_channel=False, **channel_params)
    channel4 = Channel(name='channel4', experiment=experiment2, is_channel=False, **channel_params)
    channel5 = Channel(name='channel5', experiment=experiment2, is_channel=False, **channel_params)
    channel6 = Channel(name='channel6', experiment=experiment2, is_channel=False, **channel_params)
    channelA = Channel(name='channelA', experiment=experiment1, is_channel=True, **channel_params)
    channelB = Channel(name='channelB', experiment=experiment1, is_channel=True, **channel_params)
    channelC = Channel(name='channelC', experiment=experiment2, is_channel=True, **channel_params)
    channelD = Channel(name='channelD', experiment=experiment2, is_channel=True, **channel_params)
    for obj in [channel1, channel2, channel3, channel4, channel5, channel6,
                channelA, channelB, channelC, channelD]:
        obj.save()

