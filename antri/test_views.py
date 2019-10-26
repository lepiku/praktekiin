from django.test import TestCase

class ViewsTest(TestCase):
    # test / bisa dibuka
    def test_index(self):
        response = self.client.get('/')

        self.assertContains(response, 'Fibrianti')


