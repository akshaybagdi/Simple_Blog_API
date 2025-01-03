# posts/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class CommentTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.post_url = reverse('post-list')
        self.user_data = {'username': 'testuser', 'password': 'testpass', 'email': 'testuser@example.com'}
        self.user = User.objects.create_user(**self.user_data)

    def test_create_post(self):
        login_response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass'})
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(self.post_url, {'title': 'Test Post', 'content': 'Test content.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_posts(self):
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
