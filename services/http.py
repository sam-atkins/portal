"""Local and AWS API Gateway HTTP requests to services"""
import json

from manageconf import get_config
import requests


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
        self, service_name: str, url: str, payload: dict, request_type: str = "remote"
    ):
        """Makes a HTTP request to local API or AWS API Gateway endpoint

        Args:
            service_name (str): the service to make the HTTP request to
            url (str): url for the HTTP request
            payload (dict): request body for the request
            request_type (str): enum for request, either remote, mock_server or localhost

        Returns:
            str: JSON response
        """
        if request_type == "mock_server":
            self.headers["x-api-key"] = get_config(
                f"POSTMAN_MOCK_SERVER_API_KEY_{service_name.upper()}"
            )
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
