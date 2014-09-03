from django.test import TestCase
from homepage.models import Parking
from django.contrib.auth.models import User

class AnimalTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="lorem", email="lorem@test.com",password="s")
        User.objects.create_user(username="foo", email="foo@test.com",password="s")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')