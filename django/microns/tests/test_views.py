from django.test import SimpleTestCase

class HomePageViewTestCase(SimpleTestCase):
    def test_request_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

