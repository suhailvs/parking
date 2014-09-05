from django.test import TestCase
from homepage.models import Parking
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class LoginRequiredTestCase(TestCase):
	def test_ajax_homepages(self):
		""" Test whether these url work only for logged in users"""
		from django.test import Client
		c = Client()
		response = c.get(reverse('ajax_home'), {'page': 'editprofile'})		
		self.assertEqual(response.status_code, 302)