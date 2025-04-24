import unittest
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        
    def test_register_valid_user(self):
        # Define test data for a valid user registration with new UID format
        data = {
            'username': '24MCA005',  # New UID format
            'email': 'test@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'phone': '1234567890'
        }
        
        # Check user doesn't exist before test
        self.assertFalse(User.objects.filter(username='24MCA005').exists())
        
        # Send POST request to register view
        response = self.client.post(self.register_url, data)
        
        # Check that the user was created
        self.assertTrue(User.objects.filter(username='24MCA005').exists())
        
        # Check redirect to login page
        self.assertRedirects(response, reverse('login'))
        
        # Check success message was set
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Registration successful! Please login with your credentials.")
        
        # Verify the user data was saved correctly
        user = User.objects.get(username='24MCA005')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('securepassword123'))

class LoginViewTest(TestCase):
    def setUp(self):
        # Create a test user with new UID format
        self.user = User.objects.create_user(
            username='24MCA005',  # New UID format
            email='test@example.com',
            password='password123'
        )
        self.client = Client()

    def test_successful_login(self):
        # Test successful login with valid credentials
        response = self.client.post(reverse('login'), {
            'number': '24MCA005',  # New UID format
            'password': 'password123'
        })
        
        # Check that the user is redirected to index page
        self.assertRedirects(response, reverse('index'))
        
        # Test that the user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # Check that a success message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Login successful!')

class LogoutViewTest(TestCase):
    def setUp(self):
        # Create a test user with new UID format
        self.user = User.objects.create_user(
            username='24MCA005',  # New UID format
            email='test@example.com',
            password='password123'
        )
        self.client = Client()
        
        # Log in the user
        self.client.login(username='24MCA005', password='password123')
        
    def test_logout_redirects_to_index(self):
        # Verify user is logged in before test
        self.assertTrue('_auth_user_id' in self.client.session)
        
        # Send request to logout view
        response = self.client.get(reverse('logout'))
        
        # Check that the user is no longer authenticated
        self.assertFalse('_auth_user_id' in self.client.session)
        
        # Check that the user is redirected to index page
        self.assertRedirects(response, reverse('index'))