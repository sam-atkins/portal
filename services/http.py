"""Local and AWS API Gateway HTTP requests to services"""
import json

from manageconf import get_config
import requests

from .exceptions import ServiceNotFoundError


class Http:
    """HTTP requests to local or via AWS API Gateway (Lambda Proxy)"""

    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "accept-encoding": "gzip, deflate",
            "content-length": "19",
            "Connection": "keep-alive",
            "cache-control": "no-cache",
        }

    def make_api_request(
        self,
        service_name: str,
        service_version: int,
        payload: dict,
        local_request: bool = False,
    ):
        """Makes a HTTP request to local API or AWS API Gateway endpoint

        Args:
            service_name (str): the service to make the HTTP request to
            service_version (int): version number of the service
            payload (dict): request body for the request

        Returns:
            str: JSON response
        """
        if local_request:
            self._build_local_headers(service_name=service_name)
            url = self._build_local_url(service_name=service_name)
        else:
            url = self._build_api_gateway_url(service_name=service_name)
        json_payload = json.dumps(payload)
        try:
            response = requests.request(
                "POST", url, data=json_payload, headers=self.headers
            )
            if response.status_code <= 300:
                return response.text
            else:
                response.raise_for_status
        # TODO(sam) fine tune exception handling
        except Exception as ex:
            # log to Cloudwatch
            print(ex)
            return {}

    def _build_local_headers(self, service_name: str):
        """Adds to the headers for local requests using Postman mock server

        Args:
            service_name (str): the service to make the HTTP request to
        """
        service_directory = get_config("service_directory", {})
        try:
            service_config = service_directory.get(service_name).get("local")
        except AttributeError:
            raise ServiceNotFoundError(service_directory)
        request_type = service_config.get("request_type")
        if request_type == "mock_server":
            self.headers["x-api-key"] = get_config(
                f"POSTMAN_MOCK_SERVER_API_KEY_{service_name.upper()}"
            )

    @classmethod
    def _build_local_url(cls, service_name: str) -> str:
        """Builds the localhost url for requests to local services

        Args:
            service_name (str): the service to make the HTTP request to

        Returns:
            str: url
        """
        service_directory = get_config("service_directory", {})
        try:
            service_config = service_directory.get(service_name).get("local")
        except AttributeError:
            raise ServiceNotFoundError(service_directory)
        protocol = service_config.get("protocol")
        hostname = service_config.get("hostname")
        port = service_config.get("port")
        path = service_config.get("path")
        if port is None:
            url = f"{protocol}{hostname}/{path}"
        else:
            url = f"{protocol}{hostname}:{port}/{path}"
        return url

    @classmethod
    def _build_api_gateway_url(cls, service_name: str) -> str:
        """Builds the url for requests to AWS API Gateway endpoints

        Args:
            service_name (str): the service to make the HTTP request to

        Returns:
            str: url
        """
        service_directory = get_config("service_directory", {})
        try:
            service_config = service_directory.get(service_name).get("api_gateway")
        except AttributeError:
            raise ServiceNotFoundError(service_directory)
        protocol = service_config.get("protocol")
        hostname = service_config.get("hostname")
        path = service_config.get("path")
        return f"{protocol}{hostname}/{path}"
