from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
import nada.models
from nada.fixtures import is_empty, nuke_all, boss_setup, neurons_setup, BOSS_CLASSES, NEURONS_CLASSES, NEURONS_TEST_OPTIONS
import unittest

class FixturesTestCase(APITestCase):
    
    def setUp(self):
        self.assertTrue(is_empty(BOSS_CLASSES))
        self.assertTrue(is_empty(BOSS_CLASSES))
        boss_setup()
        neurons_setup(**NEURONS_TEST_OPTIONS)
        
    def test_fixtures(self):
        for (cls, count) in [(nada.models.Collection, 1),
                             (nada.models.CoordinateFrame, 1),
                             (nada.models.Experiment, 2),
                             (nada.models.Layer, 10)]:
            found = len(cls.objects.all())
            self.assertEquals(found, count, 'Expected %s instances of %s, but found %s' % (count, cls, found))

    def test_neuron_connections(self):
        for neuron in nada.models.Neuron.objects.all():
            self.assertIsNotNone(neuron.experiment)
            self.assertIsNotNone(neuron.layer)
            self.assertEquals(neuron.layer.name, 'layer1')

    def test_synapse_connections(self):
        for synapse in nada.models.Synapse.objects.all():
            self.assertIsNotNone(synapse.experiment)
            self.assertIsNotNone(synapse.layer)
            self.assertIsNotNone(synapse.neuron)
            self.assertEquals(synapse.layer.name, 'layer2')
            self.assertIn(synapse, synapse.neuron.synapses.all())
            self.assertEquals(synapse, synapse.partner_synapse.partner_synapse)
            self.assertEquals(synapse.neuron, synapse.partner_synapse.partner_neuron)

    def tearDown(self):
        nuke_all(NEURONS_CLASSES)
        self.assertTrue(is_empty(NEURONS_CLASSES))
        nuke_all(BOSS_CLASSES)
        self.assertTrue(is_empty(BOSS_CLASSES))

