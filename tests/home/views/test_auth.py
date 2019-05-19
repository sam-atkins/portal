from django.test import TestCase


class LogInViewTestCase(TestCase):
    def test_login_view_returns_200(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_view_renders_login_template(self):
        response = self.client.get("/login/")
        self.assertTemplateUsed(response, "home/base.html", "registration/login.html")
