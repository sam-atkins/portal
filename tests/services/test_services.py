from django.test import TestCase

from services.service_proxy import ServiceProxy
from services.exceptions import ServiceFunctionNotFoundError, ServiceNotFoundError


class ServicesTestCase(TestCase):
    def test_get_service_config_returns_config(self):
        service_name = "met_service"
        service_version = 1
        service_proxy = ServiceProxy()
        service_config = service_proxy._get_service_config(
            service_name=service_name, service_version=service_version
        )
        self.assertEqual(
            service_config,
            {
                "api_gateway": {
                    "protocol": "https://",
                    "hostname": "ugly-url.execute-api.region.amazonaws.com",
                    "path": "Prod",
                },
                "lambda": {"function__weather": "met-service-weather-function"},
            },
        )

    def test_get_service_config_raises_if_unknown_service(self):
        with self.assertRaises(ServiceNotFoundError):
            service_name = "no_service"
            service_version = 1
            service_proxy = ServiceProxy()
            service_proxy._get_service_config(
                service_name=service_name, service_version=service_version
            )

    def test_determine_local_request_type_returns_localhost_str(self):
        local_config = {"request_type": "localhost"}
        service_proxy = ServiceProxy()
        local_request_type = service_proxy._determine_local_request_type(
            local_config=local_config
        )
        self.assertEqual(local_request_type, "localhost")

    def test_determine_local_request_type_returns_mock_server_str(self):
        local_config = {"request_type": "mock_server"}
        service_proxy = ServiceProxy()
        local_request_type = service_proxy._determine_local_request_type(
            local_config=local_config
        )
        self.assertEqual(local_request_type, "mock_server")

    def test_get_lambda_function_name_returns_function_name(self):
        function_name = "weather"
        lambda_config = {"function__weather": "met-service-weather-function"}
        service_proxy = ServiceProxy()
        lambda_function_name = service_proxy._get_lambda_function_name(
            function_name=function_name, lambda_config=lambda_config
        )
        expected_lambda_function_name = "met-service-weather-function"
        self.assertEqual(lambda_function_name, expected_lambda_function_name)

    def test_get_lambda_function_name_raises_if_invalid_function_name(self):
        with self.assertRaises(ServiceFunctionNotFoundError):
            function_name = "wrong"
            lambda_config = {"function__weather": "met-service-weather-function"}
            service_proxy = ServiceProxy()
            service_proxy._get_lambda_function_name(
                function_name=function_name, lambda_config=lambda_config
            )

    def test_build_url_returns_api_gateway_url(self):
        function_name = "weather"
        api_service_config = {
            "protocol": "https://",
            "hostname": "ugly-url.execute-api.region.amazonaws.com",
            "path": "Prod",
        }
        service_proxy = ServiceProxy()
        service_url = service_proxy._build_url(
            function_name=function_name, api_config=api_service_config
        )
        self.assertEqual(
            service_url,
            "https://ugly-url.execute-api.region.amazonaws.com/Prod/weather",
        )

    def test_build_url_returns_localhost_url(self):
        function_name = "weather"
        api_service_config = {
            "protocol": "http://",
            "hostname": "localhost",
            "port": "3002",
            "path": "dev",
            "request_type": "localhost",
        }
        service_proxy = ServiceProxy()
        service_url = service_proxy._build_url(
            function_name=function_name, api_config=api_service_config
        )
        self.assertEqual(service_url, "http://localhost:3002/dev/weather")
