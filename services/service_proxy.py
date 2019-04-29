"""Interface to making requests to services"""
import json

from manageconf import get_config

from .http import Http
from .aws_lambda import LambdaProxy
from .exceptions import ServiceNotFoundError


class ServiceProxy:
    """Interface to Services via local HTTP, AWS API Gateway or AWS Lambda"""

    @classmethod
    def service_request(cls, service_name: str, service_version: int, payload: dict):
        """Routes a service request to local, Lambda or API Gateway

        Args:
            service_name (str): the service to make the HTTP request to
            service_version (int): version number of the service
            payload (dict): request body for the request

        Returns:
            dict: Response from the service
        """
        service_directory = get_config("service_directory", {})
        try:
            service_config = service_directory.get(service_name, {})
        except AttributeError:
            raise ServiceNotFoundError(service_directory)
        lambda_config = service_config.get("lambda", {})
        api_gateway_config = service_config.get("api_gateway", {})

        if get_config("stage", "local") == "local":
            http = Http()
            data = http.make_api_request(
                service_name=service_name,
                service_version=service_version,
                payload=payload,
                local_request=True,
            )
        elif lambda_config:
            service_function_name = lambda_config.get("function_name")
            lambda_proxy = LambdaProxy()
            data = lambda_proxy.invoke_lambda_function(
                service_name=service_name,
                service_version=service_version,
                service_function_name=service_function_name,
                payload=payload,
            )
        elif api_gateway_config:
            http = Http()
            data = http.make_api_request(
                service_name=service_name,
                service_version=service_version,
                payload=payload,
            )

        if isinstance(data, str):
            return cls._decode(data)
        return data

    @classmethod
    def _decode(cls, json_object: str) -> dict:
        """JSON decoding to Python dictionary

        Args:
            json_object (str): the object to be decoded

        Returns:
            dict: Decoded JSON response
        """
        return json.loads(json_object)
