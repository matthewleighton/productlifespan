from django.test import SimpleTestCase
from django.urls import reverse, resolve

from products.views import index

class TestUrls(SimpleTestCase):
	def test_index_url_is_resolved(self):
		url = reverse('products:index')

		self.assertEquals(resolve(url).func, index)