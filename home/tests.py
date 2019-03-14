from django.test import TestCase
from users.models import CustomUser


class HomeViewsLoggedInUserTestCase(TestCase):
    def setUp(self):
        self.client.force_login(
            CustomUser.objects.get_or_create(username='testuser')[0])

    def test_logged_in_user_index_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_home_returns_200(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)


class HomeViewsTestCase(TestCase):
    def test_index_redirects_returns_302(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_index_redirect_follow_returns_200(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_index_directs_to_login_view(self):
        response = self.client.get('/')
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/',
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True)

    def test_home_redirects_returns_302(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 302)

    def test_home_redirect_follow_returns_200(self):
        response = self.client.get('/home/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_home_directs_to_login_view(self):
        response = self.client.get('/home/')
        self.assertRedirects(
            response=response,
            expected_url='/accounts/login/?next=/home/',
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True)
