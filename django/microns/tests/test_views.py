from django.test import TestCase, SimpleTestCase

class HomePageViewTestCase(SimpleTestCase):
    def test_request_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

# Database queries aren't allowed in SimpleTestCase; TestCase needed

class HealthCheckTestCase(TestCase):
    def test_request_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200, '/health returned %s: %s' % (response.status_code, response.content))
