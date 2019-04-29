"""Interface to making requests to services"""
import json

from manageconf import get_config

from .http import Http
from .exceptions import ServiceNotFoundError


class ServiceProxy:
    """Interface to Services via local HTTP, AWS API Gateway or AWS Lambda"""

    @classmethod
    def service_request(
        cls,
        service_name: str,
        service_version: int,
        service_function_name: str,
        payload: dict,
    ):
        """Routes a service request to local, Lambda or API Gateway

        Args:
            service_name (str): the service to make the HTTP request to
            service_version (int): version number of the service
            service_function_name (str): the Lambda function name (is this needed here?)
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
        stage = get_config("stage")

        if stage == "local":
            http = Http()
            data = http.make_api_request(
                service_name=service_name,
                service_version=service_version,
                payload=payload,
                local_request=True,
            )
        elif lambda_config:
            # TODO(sam) instantiate lambda proxy etc
            pass
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
