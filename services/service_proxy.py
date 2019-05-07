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
        service_directory = get_config("service_directory", {})
        if service_directory is None:
            # Log to CloudWatch
            print(
                f"service_directory is {service_directory}, validate param store config"
            )
        try:
            service_config = service_directory.get(
                f"{service_name}__v{service_version}", {}
            )
        except AttributeError:
            raise ServiceNotFoundError(service_directory)
        lambda_config = service_config.get("lambda", {})
        api_gateway_config = service_config.get("api_gateway", {})
        data = {}

        if get_config("stage", "local") == "local":
            http = Http()
            data = http.make_api_request(
                service_name=service_name,
                service_version=service_version,
                payload=payload,
                local_request=True,
            )
        elif lambda_config:
            service_function_name = cls._get_lambda_function_name(
                function_name=function_name, lambda_config=lambda_config
            )
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
                function_name=function_name,
                payload=payload,
            )

        if isinstance(data, str):
            return cls._decode(data)
        return data

    # TODO(sam) get service config helper method
    # TODO(sam) build api gateway url helper method

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
    def _decode(cls, json_object: str) -> dict:
        """JSON decoding to Python dictionary

        Args:
            json_object (str): the object to be decoded

        Returns:
            dict: Decoded JSON response
        """
        return json.loads(json_object)
