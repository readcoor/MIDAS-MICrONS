import os
import unittest
from nada.boss_client import BossClient
from django.conf import settings

class TheBossTestCase(unittest.TestCase):

    def test_assumptions(self):
        'confirm we have a config file for TheBoss'
        config_file = settings.THEBOSS_CONFIG
        self.assertTrue(os.path.exists(config_file))

    def test_get_collection(self):
        boss = BossClient()
        collection = boss.get_collection('collection1')
        self.assertEquals(collection.name, 'collection1')
        
    def test_get_experiment(self):
        boss = BossClient()
        experiment = boss.get_experiment('experiment1', 'collection1')
        self.assertEquals(experiment.name, 'experiment1')

    def test_get_channel(self):
        boss = BossClient()
        channel = boss.get_channel('channel1', 'collection1', 'experiment1')
        self.assertEquals(channel.name, 'channel1')
    
