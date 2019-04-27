"""Local and AWS API Gateway HTTP requests to services"""
import json

from manageconf import get_config
import requests

# from requests.exceptions import HTTPError


class Http:
    """HTTP requests to local or via AWS API Gateway (Lambda Proxy)"""

    @classmethod
    def make_local_request(cls, service_name: str, service_version: int, payload: dict):
        """Makes a HTTP request to a locally running service

        Args:
            service_name (str): the service to make the HTTP request to
            service_version (int): version number of the service
            service_function_name (str): the Lambda function name (is this needed here?)
            payload (dict): request body for the request

        Returns:
            str: JSON response from the service
        """
        url = cls._build_local_url(service_name=service_name)
        json_payload = json.dumps({"name": "ldn"})
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "accept-encoding": "gzip, deflate",
            "content-length": "19",
            "Connection": "keep-alive",
            "cache-control": "no-cache",
        }
        try:
            response = requests.request("POST", url, data=json_payload, headers=headers)
            if response.status_code <= 300:
                return response.text
            else:
                response.raise_for_status
        except Exception as ex:
            # urllib3.exceptions.NewConnectionError
            # except HTTPError as ex:
            # log to Cloudwatch
            print(ex)
            return {}

    @classmethod
    def _build_local_url(cls, service_name: str) -> str:
        """Builds the localhost url for requests to local services

        Args:
            service_name (str): the service to make the HTTP request to

        Returns:
            str: the url
        """
        local_service_directory = get_config("local_service_directory", {})
        try:
            service_config = local_service_directory.get(service_name).get("local")
        except AttributeError:
            local_services_with_config = ", ".join(list(local_service_directory.keys()))
            raise Exception(
                f"Service not found. Local services with config "
                f"are: {local_services_with_config}"
            )

        protocol = service_config.get("protocol")
        hostname = service_config.get("hostname")
        port = service_config.get("port")
        path = service_config.get("path")
        if port is None:
            url = f"{protocol}{hostname}{path}"
        else:
            url = f"{protocol}{hostname}{port}{path}"

        return url
