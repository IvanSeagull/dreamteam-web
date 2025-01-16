# api/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from api.models import FriendRequest, Friend

CustomUser = get_user_model()


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

        self.assertRedirects(response, f"{self.profile_url}/newuser", fetch_redirect_response=False)
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
        self.assertRedirects(response, f"{self.profile_url}/testuser", fetch_redirect_response=False)
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


class FriendFunctionalityTests(TestCase):
    def setUp(self):
        self.client = Client()


        self.user1 = CustomUser.objects.create_user(username='user1', email="email1@gmail.com", password='password1', name='User One')
        self.user2 = CustomUser.objects.create_user(username='user2', email="email2@gmail.com", password='password2', name='User Two')
        self.user3 = CustomUser.objects.create_user(username='user3', email="email3@gmail.com", password='password3', name='User Three')

        self.client.login(username='user1', password='password1')

    def test_send_friend_request(self):
        response = self.client.post(
            reverse('send_friend_request'),
            data={'receiver_id': self.user2.id},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FriendRequest.objects.count(), 1)
        self.assertEqual(FriendRequest.objects.first().receiver, self.user2)

    def test_send_friend_request_to_self(self):
        response = self.client.post(
            reverse('send_friend_request'),
            data={'receiver_id': self.user1.id},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(FriendRequest.objects.count(), 0)

    def test_send_duplicate_friend_request(self):
        FriendRequest.objects.create(sender=self.user1, receiver=self.user2)
        response = self.client.post(
            reverse('send_friend_request'),
            data={'receiver_id': self.user2.id},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Friend request already sent', response.json()['error'])

    def test_get_friends(self):
        Friend.objects.create(first_user=self.user1, second_user=self.user2)
        response = self.client.get(reverse('get_friends') + f'?username={self.user1.username}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['friends']), 1)
        self.assertEqual(response.json()['friends'][0]['username'], self.user2.username)

    def test_get_friend_requests(self):
        FriendRequest.objects.create(sender=self.user2, receiver=self.user1)
        response = self.client.get(reverse('get_friend_requests'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['requests']), 1)
        self.assertEqual(response.json()['requests'][0]['sender_username'], self.user2.username)

    def test_accept_friend_request(self):
        friend_request = FriendRequest.objects.create(sender=self.user2, receiver=self.user1)
        response = self.client.post(reverse('accept_friend_request', args=[friend_request.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Friend.objects.count(), 1)
        self.assertEqual(FriendRequest.objects.count(), 0)

    def test_reject_friend_request(self):
        friend_request = FriendRequest.objects.create(sender=self.user2, receiver=self.user1)
        response = self.client.post(reverse('reject_friend_request', args=[friend_request.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Friend.objects.count(), 0)
        self.assertEqual(FriendRequest.objects.count(), 0)

    def test_accept_non_existing_friend_request(self):
        response = self.client.post(reverse('accept_friend_request', args=[999]))
        self.assertEqual(response.status_code, 404)
        self.assertIn('Friend request not found', response.json()['error'])

    def test_reject_non_existing_friend_request(self):
        response = self.client.post(reverse('reject_friend_request', args=[999]))
        self.assertEqual(response.status_code, 404)
        self.assertIn('Friend request not found', response.json()['error'])