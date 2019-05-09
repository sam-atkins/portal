"""Interface to making requests to services"""
import json

from manageconf import get_config

from .http import Http
from .aws_lambda import LambdaProxy
from .exceptions import ServiceNotFoundError, ServiceFunctionNotFoundError


class ServiceProxy:
    """Interface to Services via local HTTP, AWS API Gateway or AWS Lambda"""

    @classmethod
    def service_request(
        cls, service_name: str, service_version: int, function_name: str, payload: dict
    ):
        """Routes a service request to local, Lambda or API Gateway

        Args:
            service_name (str): the service to make the HTTP request to
            service_version (int): version number of the service
            function_name (str): name of the function to invoke
            payload (dict): request body for the request

        Returns:
            dict: Response from the service
        """
        service_config = cls._get_service_config(
            service_name=service_name, service_version=service_version
        )
        lambda_config = service_config.get("lambda", {})
        api_gateway_config = service_config.get("api_gateway", {})
        data = {}

        if get_config("stage", "local") == "local":
            local_config = service_config.get("local", {})
            local_request_type = cls._determine_local_request_type(
                local_config=local_config
            )
            url = cls._build_url(function_name=function_name, api_config=local_config)
            http = Http()
            data = http.make_api_request(
                service_name=service_name,
                url=url,
                payload=payload,
                request_type=local_request_type,
            )
        elif lambda_config:
            service_function_name = cls._get_lambda_function_name(
                function_name=function_name, lambda_config=lambda_config
            )
            lambda_proxy = LambdaProxy()
            data = lambda_proxy.invoke_lambda_function(
                service_function_name=service_function_name, payload=payload
            )
        elif api_gateway_config:
            url = cls._build_url(
                function_name=function_name, api_config=api_gateway_config
            )
            http = Http()
            data = http.make_api_request(
                service_name=service_name, url=url, payload=payload
            )

        if isinstance(data, str):
            return cls._decode(data)
        return data

    @classmethod
    def _get_service_config(cls, service_name: str, service_version: int) -> dict:
        service_directory = get_config("service_directory", {})
        try:
            service_config = service_directory.get(
                f"{service_name}__v{service_version}"
            )
        except AttributeError:
            raise ServiceNotFoundError(service_directory)
        if service_config is None:
            raise ServiceNotFoundError(service_directory)
        return service_config

    @classmethod
    def _determine_local_request_type(cls, local_config: dict):
        """Determines if local request is local Docker network or Postman mock server

        Args:
            local_config (dict): local http config

        Returns:
            str: enum, either mock_server or localhost
        """
        request_type = local_config.get("request_type")
        if request_type == "mock_server":
            return "mock_server"
        else:
            return "localhost"

    @classmethod
    def _get_lambda_function_name(cls, function_name: str, lambda_config: dict):
        """Gets the Lambda function from service directory lambda config

        Args:
            function_name (str): the function name received from the client
            lambda_config (dict): config with key/value pairs of Lambda functions

        Returns:
            str: Lambda function name
        """
        service_function_name = lambda_config.get(f"function__{function_name}")
        if service_function_name is None:
            raise ServiceFunctionNotFoundError(lambda_config)
        return service_function_name

    @classmethod
    def _build_url(cls, function_name: str, api_config: dict) -> str:
        """Builds the url for requests to AWS API Gateway endpoints

        Args:
            service_name (str): the service to make the HTTP request to
            api_config (dict): HTTP request config

        Returns:
            str: url
        """
        protocol = api_config.get("protocol")
        hostname = api_config.get("hostname")
        port = api_config.get("port")
        path = api_config.get("path")
        if port is None:
            url = f"{protocol}{hostname}/{path}/{function_name}"
        elif path is None:
            url = f"{protocol}{hostname}:{port}/{function_name}"
        else:
            url = f"{protocol}{hostname}:{port}/{path}/{function_name}"
        return url

    @classmethod
    def _decode(cls, json_object: str) -> dict:
        """JSON decoding to Python dictionary

        Args:
            json_object (str): the object to be decoded

        Returns:
            dict: Decoded JSON response
        """
        return json.loads(json_object)
