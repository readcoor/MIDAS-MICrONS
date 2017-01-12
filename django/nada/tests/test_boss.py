# You can view/edit these resources interactively by visiting
# https://api.theboss.io/v0.7/mgmt/resources

# PREREQUISITES:
# As specified in nada.remote, you must provide a valid token in the
# configuration file "theboss.cfg"

import os
import unittest
from nada.remote import Remote, CONFIG
from intern.resource.boss.resource import CoordinateFrameResource, CollectionResource, ExperimentResource, ChannelResource

COLLECTION = 'TEST_COLLECTION'
COORD_FRAME = 'TEST_COORDINATE_FRAME'
EXPERIMENT = 'Mouse42'
CHANNEL = 'EM'
ANN_CHANNEL = 'Algorithm1'

class TheBossTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''Initialized once, before any class tests are run'''
        boss = cls.boss = Remote()
        fixtures = {}
        fixtures['coordframe'] = CoordinateFrameResource(COORD_FRAME)
        fixtures['collection'] = CollectionResource(COLLECTION)
        fixtures['experiment'] = ExperimentResource(EXPERIMENT, COLLECTION, coord_frame=COORD_FRAME)
        fixtures['channel'] = ChannelResource(CHANNEL, COLLECTION, EXPERIMENT, 'image')
        fixtures['ann_channel'] = ChannelResource(ANN_CHANNEL, COLLECTION, EXPERIMENT, 'annotation',
                                                  sources=[CHANNEL])
        cls.fixtures = fixtures
        for resource_name in ['coordframe', 'collection', 'experiment', 'channel', 'ann_channel']:
            boss.create_project(fixtures[resource_name])

    @classmethod
    def tearDownClass(cls):
        '''Remove items. Use reverse order due to dependencies.'''
        boss = cls.boss
        fixtures = cls.fixtures
        for resource_name in ['ann_channel', 'channel', 'experiment', 'collection', 'coordframe']:
            boss.delete_project(fixtures[resource_name])
        cls.assertNotIn(cls, COLLECTION, boss.list_collections())
        cls.assertNotIn(cls, COORD_FRAME, boss.list_coordinate_frames())

    def test_config_file(self):
        'confirm we have a config file for TheBoss'
        self.assertTrue(os.path.exists(CONFIG))

    def test_collections(self):
        collections = self.boss.list_collections()
        self.assertIn(COLLECTION, collections)

    def test_coord_frames(self):
        coord_frames = self.boss.list_coordinate_frames()
        self.assertIn(COORD_FRAME, coord_frames)
        
    def test_experiments(self):
        experiments = self.boss.list_experiments(COLLECTION)
        self.assertIn(EXPERIMENT, experiments)
        self.assertEquals(len(experiments), 1)
    
    def test_channels(self):
        channels = self.boss.list_channels(COLLECTION, EXPERIMENT)
        self.assertIn(CHANNEL, channels)
        self.assertIn(ANN_CHANNEL, channels)
        self.assertEquals(len(channels), 2)
