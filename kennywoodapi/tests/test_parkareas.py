import unittest
from django.test import TestCase
from django.urls import reverse
from ..models import ParkArea, Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestParkAreas(TestCase): 
    # SET UP SELF 
    # This set up acts as the test user that will be performing the requests
    def setUp(self):
        self.username = 'TestUser'
        self.password = 'Test123'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=1, family_members=9)

    def testPostParkArea(self):
        # STEP 1: SET UP DATA
        # We need to set up the data that we are going to be posting
        # Since this is a post, we do not need to CREATE the data
        # Post will be doing that for us!
        new_parkarea = {
            "name": "Test Park 1", 
            "theme": "The best theme ever"
        }
        # STEP 2: MAKE REQUEST/PERFORM ACTION
        # Depending on the kind of request we want, we will be posting directly from the URL 
        # Given the URL, body, and header 
            # The URL will be where we are reversing posting from
            # The dictionary we want to be sent to the API will be the body 
            # The header will have the token
            # Django needs -list in order to know that it will be going back to the list method
        response = self.client.post(
            reverse('parkarea-list'), new_parkarea, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        # STEP 3: MAKE ASSERIONS
        self.assertEqual(response.status_code, 200)

        self.assertEqual(ParkArea.objects.count(), 1)
