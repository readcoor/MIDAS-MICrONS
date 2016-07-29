from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
import nada.models
from nada.fixtures import is_empty, nuke_all, boss_setup, neurons_setup, \
     BOSS_CLASSES, NEURONS_CLASSES, NEURONS_TEST_OPTIONS


class NdaIcdTestCase(APITestCase):
    
    def setUp(self):
        self.assertTrue(is_empty(BOSS_CLASSES))
        self.assertTrue(is_empty(BOSS_CLASSES))
        boss_setup()
        neurons_setup(**NEURONS_TEST_OPTIONS)

    def test_S1_is_synapse(self):
        for s_id in [12, 42, 99]: # random test values of actual synapses
            url = reverse('is_synapse', args=['collection1', 'experiment1', 'layer2', s_id])
            self.assertEquals(url, '/is_synapse/collection1/experiment1/layer2/%s' % s_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            result = response.data
            self.assertEquals(True, result.get('result', None))

    def test_S1_is_synapse_invalid(self):
        for s_id in [1012, 1042, 9999]: # random test values of invalid synapse IDs
            url = reverse('is_synapse', args=['collection1', 'experiment1', 'layer2', s_id])
            self.assertEquals(url, '/is_synapse/collection1/experiment1/layer2/%s' % s_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_S1_is_synapse_wrong_object(self):
        for s_id in [12, 32, 43]: # random test values of actual synapses
            url = reverse('is_synapse', args=['collection1', 'experiment1', 'layer1', s_id])
            self.assertEquals(url, '/is_synapse/collection1/experiment1/layer1/%s' % s_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            result = response.data
            # find a neuron instead of a synapse, return False
            self.assertEquals(False, result.get('result', None))

    def test_S2_synapse_ids(self):
        url = reverse('synapse_ids', args=['collection1', 'experiment1', 'layer2', 0, 0, 50, 0, 2000, 0, 2000])
        self.assertEquals(url, '/synapse_ids/collection1/experiment1/layer2/0/0,50/0,2000/0,2000')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        result = response.data.get('ids', None)
        self.assertIsInstance(result, list)
        for id in result: self.assertIsInstance(id, int)

    def test_S3_synapse_keypoint(self):
        for synapse in nada.models.Synapse.objects.all():
            synapse_id = synapse.name
            url = reverse('synapse_keypoint', args=['collection1', 'experiment1', 'layer2', 0, synapse_id])
            self.assertEquals(url, '/synapse_keypoint/collection1/experiment1/layer2/0/%s' % synapse_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            result = response.data.get('keypoint', None)
            self.assertIsInstance(result, tuple)
            synapse_kp = synapse.keypoint
            self.assertEquals(result[0], synapse_kp.x)
            self.assertEquals(result[1], synapse_kp.y)
            self.assertEquals(result[2], synapse_kp.z)

    def test_S4_synapse_parent(self):
        for synapse in nada.models.Synapse.objects.all():
            synapse_id = synapse.name
            url = reverse('synapse_parent', args=['collection1', 'experiment1', 'layer2', synapse_id])
            self.assertEquals(url, '/synapse_parent/collection1/experiment1/layer2/%s' % synapse_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            result = response.data.get('parent_neurons', None)
            self.assertIsInstance(result, dict)
            # each synapse should have exactly one pre-synapse neuron and one post-synapse neuron
            self.assertEquals(len(result), 2)
            self.assertIn(nada.models.Polarity.pre.value, result.values())
            self.assertIn(nada.models.Polarity.post.value, result.values())

            for (neuron_id, polarity) in result.items():
                self.assertIsInstance(polarity, int)
                self.assertIn(polarity, range(0,4))
                neuron = nada.models.Neuron.get_by_name(int(neuron_id))
                if synapse.polarity == polarity:
                    self.assertEquals(synapse.neuron.name, neuron.name)
                    self.assertIsNotNone(neuron.synapses.filter(name=synapse_id).get())
                else:
                    self.assertEquals(synapse.partner_neuron.name, neuron.name)

    def test_S5_is_neuron(self):
        for n_id in [12, 32, 49]: # random test values of actual neurons
            url = reverse('is_neuron', args=['collection1', 'experiment1', 'layer1', n_id])
            self.assertEquals(url, '/is_neuron/collection1/experiment1/layer1/%s' % n_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            result = response.data
            self.assertEquals(True, result.get('result', None))

    def test_S5_is_neuron_invalid(self):
        for n_id in [1012, 1042, 9999]: # random test values of invalid neuron IDs
            url = reverse('is_neuron', args=['collection1', 'experiment1', 'layer1', n_id])
            self.assertEquals(url, '/is_neuron/collection1/experiment1/layer1/%s' % n_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_S5_is_neuron_wrong_object(self):
        for n_id in [12, 32, 49]: # random test values of actual neurons
            url = reverse('is_neuron', args=['collection1', 'experiment1', 'layer2', n_id])
            self.assertEquals(url, '/is_neuron/collection1/experiment1/layer2/%s' % n_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            result = response.data
            # found synapse instead of neuron, return False
            self.assertEquals(False, result.get('result', None))

    def test_S6_neuron_ids(self):
        url = reverse('neuron_ids', args=['collection1', 'experiment1', 'layer1', 0, 0, 50, 0, 2000, 0, 2000])
        self.assertEquals(url, '/neuron_ids/collection1/experiment1/layer1/0/0,50/0,2000/0,2000')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        result = response.data.get('ids', None)
        self.assertIsInstance(result, list)
        for id in result: self.assertIsInstance(id, int)

    def test_S7_neuron_keypoint(self):
        for neuron in nada.models.Neuron.objects.all():
            neuron_id = neuron.name
            url = reverse('neuron_keypoint', args=['collection1', 'experiment1', 'layer1', 0, neuron_id])
            self.assertEquals(url, '/neuron_keypoint/collection1/experiment1/layer1/0/%s' % neuron_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            result = response.data.get('keypoint', None)
            self.assertIsInstance(result, tuple)
            neuron_kp = neuron.keypoint
            self.assertEquals(result[0], neuron_kp.x)
            self.assertEquals(result[1], neuron_kp.y)
            self.assertEquals(result[2], neuron_kp.z)

    def test_S8_neuron_children(self):
        for neuron in nada.models.Neuron.objects.all():
            neuron_id = neuron.name
            url = reverse('neuron_children', args=['collection1', 'experiment1', 'layer1', 0,
                                                   0, 50, 0, 2000, 0, 2000, neuron_id])
            self.assertEquals(url, '/neuron_children/collection1/experiment1/layer1/0/0,50/0,2000/0,2000/%s' % neuron_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            result = response.data.get('child_synapses', None)
            self.assertIsInstance(result, dict)

            for (synapse_id, polarity) in result.items():
                self.assertIsInstance(polarity, int)
                self.assertIn(polarity, range(0,4))
                synapse = nada.models.Synapse.get_by_name(int(synapse_id))
                self.assertEquals(synapse.polarity, polarity)
                self.assertIn(neuron.name, [synapse.partner_neuron.name, synapse.neuron.name])

    def test_S9_voxel_list(self):
        for neuron in nada.models.Neuron.objects.all():
            neuron_id = neuron.name
            url = reverse('voxel_list', args=['collection1', 'experiment1', 'layer1', 0,
                                              0, 50, 0, 2000, 0, 2000, neuron_id])
            self.assertEquals(url, '/voxel_list/collection1/experiment1/layer1/0/0,50/0,2000/0,2000/%s' % neuron_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            result = response.data
            self.assertIsInstance(result, dict)
            self.assertEquals(len(result), 3)
            n_values = len(result.get('x'))
            for coord in 'xyz':
                self.assertIn(coord, result)
                values = result.get(coord, None)
                self.assertEquals(len(values), n_values)
            values = [result[c] for c in 'xyz']
            for voxel in zip(*values):
                self.assertTrue(Point(voxel).within(neuron.geometry))

    def test_SA1_synapse_compartment(self):
        for synapse in nada.models.Synapse.objects.all():
            synapse_id = synapse.name
            url = reverse('synapse_compartment', args=['collection1', 'experiment1', 'layer2', synapse_id])
            self.assertEquals(url, '/synapse_compartment/collection1/experiment1/layer2/%s' % synapse_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            self.assertIsInstance(response.data, dict)
            self.assertEquals(len(response.data), 1)
            result = response.data.get('compartment', None)
            self.assertIsInstance(result, str)
            self.assertEquals(result, nada.models.Compartment(synapse.compartment).name)

    def test_SA2_neuron_celltype(self):
        for neuron in nada.models.Neuron.objects.all():
            neuron_id = neuron.name
            url = reverse('neuron_celltype', args=['collection1', 'experiment1', 'layer1', neuron_id])
            self.assertEquals(url, '/neuron_celltype/collection1/experiment1/layer1/%s' % neuron_id)
            response = self.client.get(url, format='json')
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            self.assertIsInstance(response.data, dict)
            self.assertEquals(len(response.data), 1)
            result = response.data.get('cell_type', None)
            self.assertIsInstance(result, str)
            self.assertEquals(result, nada.models.CellType(neuron.cell_type).name)            

    def tearDown(self):
        nuke_all(NEURONS_CLASSES)
        self.assertTrue(is_empty(NEURONS_CLASSES))
        nuke_all(BOSS_CLASSES)
        self.assertTrue(is_empty(BOSS_CLASSES))
