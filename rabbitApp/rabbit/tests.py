from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


# Create your tests here.
class UserCreationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='acano', password='12345password')

    def test_user_exists(self):
        user = User.objects.get(username="acano")
        e_username = f'{user.username}'
        self.assertEqual(e_username, 'acano')
        self.assertEquals(user.check_password("12345password"), True)

    def test_register_view_success(self):
        response = self.client.post(reverse('register'),
                                    {'username': 'acano', 'password1': '940411cano', 'password2': '940411cano'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ok')

    def rest_register_view_fail(self):
        response = self.client.post(reverse('register'),
                                    {'username': 'acano', 'password1': '940411cano', 'password2': '940411cano'})

        self.assertEqual(response.status_code, 500)
