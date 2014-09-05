from django.test import TestCase
from homepage.models import Parking,Weeks
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class LoginRequiredTestCase(TestCase):
	def test_ajax_homepages(self):
		""" Test whether these url work only for logged in users"""
		from django.test import Client
		c = Client()
		response = c.get(reverse('ajax_home'), {'page': 'editprofile'})		
		self.assertEqual(response.status_code, 302)

class ListParkingTestCase(TestCase):
	fixtures = ['somedata.json']
	def setUp(self):
		self.user1=User.objects.create_user(username="lorem", email="lorem@test.com",password="s")
		self.user2=User.objects.create_user(username="foo", email="foo@test.com",password="s")
        

	def test_listparking(self):
		"""Test the ways in which parking can be listed"""

		p1=Parking(user=self.user1,
        	fromtime=4,
        	totime=6,
        	totalspaces=4,        	
        	lat='34',
        	lng='43',
        	description='good parking',
        	streetaddress='usa')
		#pic,date_added,status
		p1.save()
		# add some weeks:
		for wk in ['sunday','saturday']:
			p1.days.add(Weeks.objects.get(name=wk))

		owner = Parking.objects.get(user__username="lorem")
		self.assertEqual(owner.user.email, 'lorem@test.com')
		self.assertEqual(owner.user.is_active, True)

	def test_fromTime_toTime(self):
		"""
		Test what type of fromtime and totime possible:
		-----------------------------------------------

			* fromtime > totime which must not be allowed

		"""
		pass