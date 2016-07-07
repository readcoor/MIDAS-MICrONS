import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
import nada.models
import nada.fixtures

class FixturesTestCase(APITestCase):

    def setUp(self):
        self.assertTrue(nada.fixtures.is_empty())
        nada.fixtures.setup()
        
    def test_fixtures(self):
        for (cls, count) in [(nada.models.Collection, 1),
                             (nada.models.CoordinateFrame, 1),
                             (nada.models.Experiment, 2),
                             (nada.models.Layer, 10)]:
            found = len(cls.objects.all())
            self.assertEquals(found, count, 'Expected %s instances of %s, but found %s' % (count, cls, found))


    def test_api_get_experiment(self):
        url = reverse('experiment-detail', args=['collection1', 'experiment1'])
        self.assertEquals(url, '/v1/resource/experiment/collection1/experiment1')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get('name', None), 'experiment1')

    def test_api_get_layer(self):
        url = reverse('layer-detail', args=['collection1', 'experiment2', 'layer4'])
        self.assertEquals(url, '/v1/resource/layer/collection1/experiment2/layer4')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get('name', None), 'layer4')

    def tearDown(self):
        nada.fixtures.nuke_all()
        self.assertTrue(nada.fixtures.is_empty())

