"""Interface to making requests to services"""
import json

from manageconf import get_config

from .http import Http


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
        if cls._is_local:
            http = Http()
            data = http.make_local_request(
                service_name=service_name,
                service_version=service_version,
                payload=payload,
            )
            if isinstance(data, str):
                decoded_data = cls._decode(data)
                return decoded_data
            return data

    @classmethod
    def _is_local(cls):
        """Determines if stage is local

        Returns:
            bool: Returns true if stage is local
        """
        stage = get_config("stage")
        if stage == "local":
            return True

    @classmethod
    def _decode(cls, json_object: str) -> dict:
        """JSON decoding to Python dictionary

        Args:
            json_object (str): the object to be decoded

        Returns:
            dict: Decoded JSON response
        """
        return json.loads(json_object)
