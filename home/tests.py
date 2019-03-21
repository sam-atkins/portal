from django.test import TestCase
from users.models import CustomUser


class HomeViewsLoggedInUserTestCase(TestCase):
    def setUp(self):
        self.client.force_login(
            CustomUser.objects.get_or_create(username='testuser')[0])

    def test_logged_in_user_index_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # TODO(sam) refine this test and others once home view develops
    # ie what is rendered for logged in vs logged out user
    def test_logged_in_user_index_renders_home_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/base.html', 'home/home.html')

    def test_logged_in_user_home_returns_200(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_home_renders_home_html(self):
        response = self.client.get('/home/')
        self.assertTemplateUsed(response, 'home/base.html', 'home/home.html')


class HomeViewsTestCase(TestCase):
    def test_index_redirect_follow_returns_200(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logged_out_user_index_renders_login_html(self):
        response = self.client.get('/', follow=True)
        self.assertTemplateUsed(response, 'home/base.html',
                                'registration/login.html')

    def test_home_redirects_returns_302(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 302)

    def test_logged_out_user_home_renders_login_html(self):
        response = self.client.get('/', follow=True)
        self.assertTemplateUsed(response, 'home/base.html',
                                'registration/login.html')
