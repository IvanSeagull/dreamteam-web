# api/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login_view')
        self.profile_url = 'http://localhost:5173/profile'
        
        self.User = get_user_model()

        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            name='Test User',
            date_of_birth='1990-01-01'
        )

    # --- Signup Success ---
    def test_signup_success(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'name': 'New User',
            'date_of_birth': '1990-01-01',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
            'next': self.profile_url
        })

        self.assertRedirects(response, self.profile_url, fetch_redirect_response=False)
        self.assertTrue(self.User.objects.filter(username='newuser').exists())

    # --- Signup Failure Tests ---

    def test_signup_missing_username(self):
        response = self.client.post(self.signup_url, {
            'username': '',
            'email': 'user@example.com',
            'name': 'User Name',
            'date_of_birth': '1990-01-01',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
            'next': self.profile_url
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.User.objects.filter(email='user@example.com').exists())
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertEqual(form.errors['username'], ['This field is required.'])

    def test_signup_invalid_email(self):
        response = self.client.post(self.signup_url, {
            'username': 'user2',
            'email': 'invalidemail',
            'name': 'User Two',
            'date_of_birth': '1990-01-01',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
            'next': self.profile_url
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.User.objects.filter(email='invalidemail').exists())
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

    def test_signup_weak_password(self):
        response = self.client.post(self.signup_url, {
            'username': 'user3',
            'email': 'user3@example.com',
            'name': 'User Three',
            'date_of_birth': '1990-01-01',
            'password1': 'pass',
            'password2': 'pass',
            'next': self.profile_url
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.User.objects.filter(email='user3@example.com').exists())
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('password2', form.errors)
        self.assertIn('This password is too short. It must contain at least 8 characters.', form.errors['password2'])
        self.assertIn('This password is too common.', form.errors['password2'])

    # --- Login Tests ---

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123',
            'next': self.profile_url
        })
        self.assertRedirects(response, self.profile_url, fetch_redirect_response=False)
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
            'next': self.profile_url
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertEqual(
            form.non_field_errors(),
            ['Please enter a correct username and password. Note that both fields may be case-sensitive.']
        )
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)
