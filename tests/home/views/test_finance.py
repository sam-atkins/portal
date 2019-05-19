from unittest.mock import patch

from django.test import TestCase

from home.views.finance import build_finance_view_context
from tests.datasets.finance_data import FX_CONVERSION_DATA
from users.models import CustomUser


class FinanceViewLoggedOutUserTestCase(TestCase):
    def test_finance_view_redirects(self):
        response = self.client.get("/finance/")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "home/finance_page.html")

    def test_logged_out_user_finance_view_renders_login_html(self):
        response = self.client.get("/finance/", follow=True)
        self.assertTemplateNotUsed(response, "home/finance_page.html")


class FinanceViewLoggedInUserTestCase(TestCase):
    def setUp(self):
        self.client.force_login(
            CustomUser.objects.get_or_create(username="testuser")[0]
        )

    @patch(
        "home.views.finance.ServiceProxy.service_request",
        return_value=FX_CONVERSION_DATA,
    )
    def test_logged_in_user_finance_view_returns_200(self, mock_service_proxy):
        response = self.client.get("/finance/")
        self.assertEqual(response.status_code, 200)

    @patch(
        "home.views.finance.ServiceProxy.service_request",
        return_value=FX_CONVERSION_DATA,
    )
    def test_logged_in_user_finance_renders_finance_html(self, mock_service_proxy):
        response = self.client.get("/finance/")
        self.assertTemplateUsed(response, "home/base.html", "home/finance_page.html")


class FinanceViewHelpersTestCase(TestCase):
    def test_build_finance_view_context_returns_full_context(self):
        base_currency = "GBP"
        base_amount = 10
        result_amount = 11.1940
        result_currency = "EUR"
        context = build_finance_view_context(
            base_currency=base_currency,
            base_amount=base_amount,
            result_amount=result_amount,
            result_currency=result_currency,
        )
        self.assertEqual(
            context,
            {
                "fx": True,
                "base_amount": 10,
                "base_currency": "GBP",
                "result_amount": 11.19,
                "result_currency": "EUR",
            },
        )

    def test_build_finance_view_context_returns_context_if_result_is_None(self):
        base_currency = "GBP"
        base_amount = 10
        result_amount = None
        result_currency = "EUR"
        context = build_finance_view_context(
            base_currency=base_currency,
            base_amount=base_amount,
            result_amount=result_amount,
            result_currency=result_currency,
        )
        self.assertEqual(context, {"fx_error": True})
