from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
import nada.models
from nada.fixtures import is_empty, nuke_all, boss_setup, neurons_setup, BOSS_CLASSES, NEURONS_CLASSES, NEURONS_TEST_OPTIONS
import unittest

class FixturesTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        '''Initialized once, before any class tests are run'''
        cls.assertTrue(cls, is_empty(BOSS_CLASSES))
        cls.assertTrue(cls, is_empty(BOSS_CLASSES))
        boss_setup()
        neurons_setup(**NEURONS_TEST_OPTIONS)
        
    def test_fixtures(self):
        for (cls, count) in [(nada.models.Collection, 1),
                             (nada.models.CoordinateFrame, 1),
                             (nada.models.Experiment, 2),
                             (nada.models.Channel, 10),
                             (nada.models.Neuron, NEURONS_TEST_OPTIONS['N_NEURONS']),
                             (nada.models.Synapse, NEURONS_TEST_OPTIONS['N_SYNAPSES'])
                             ]:
            found = len(cls.objects.all())
            self.assertEquals(found, count, 'Expected %s instances of %s, but found %s' % (count, cls, found))

    def test_neuron_connections(self):
        for neuron in nada.models.Neuron.objects.all():
            self.assertIsNotNone(neuron.experiment)
            self.assertIsNotNone(neuron.channel)
            self.assertEquals(neuron.channel.name, 'channel1')

    def test_synapse_connections(self):
        for synapse in nada.models.Synapse.objects.all():
            self.assertIsNotNone(synapse.experiment)
            self.assertIsNotNone(synapse.channel)
            self.assertIsNotNone(synapse.neuron)
            self.assertIsNotNone(synapse.partner_synapse)
            self.assertEquals(synapse.channel.name, 'channel2')
            self.assertIn(synapse, synapse.neuron.synapses.all())
            self.assertEquals(synapse, synapse.partner_synapse.partner_synapse)
            self.assertEquals(synapse.neuron, synapse.partner_synapse.partner_neuron)

    def test_neuron_activity(self):
        for neuron in nada.models.Neuron.objects.all():
            na_activity = nada.models.NeuronActivity.get_by_time(neuron.experiment, neuron, 0, 1000)
            n_activity = neuron.activity.all()
            self.assertEquals(len(na_activity), len(n_activity))
            self.assertEquals(NEURONS_TEST_OPTIONS['N_ACTIVITY_ENTRIES'], len(n_activity))

    @classmethod
    def tearDownClass(cls):
        nuke_all(NEURONS_CLASSES)
        cls.assertTrue(cls, is_empty(NEURONS_CLASSES))
        nuke_all(BOSS_CLASSES)
        cls.assertTrue(cls, is_empty(BOSS_CLASSES))

