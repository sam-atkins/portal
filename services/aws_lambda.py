"""AWS Lambda invocations to services"""
import json

import boto3


class LambdaProxy:
    """Invokes requests to Lambda functions"""

    def invoke_lambda_function(
        self,
        service_name: str,
        service_version: int,
        service_function_name: str,
        payload: dict,
    ):
        """Invoke a Lambda function

        Args:
            service_name (str): the service to make the HTTP request to
            service_version (int): version number of the service (currently unused)
            service_function_name (str): the Lambda function name
            payload (dict): request body for the request

        Returns:
            dict: Lambda function response
        """
        client = boto3.client("lambda")
        json_payload = json.dumps({"body": payload})
        try:
            response = client.invoke(
                FunctionName=service_function_name, Payload=json_payload
            )
            status_code = response.get("StatusCode")
            if status_code == 200:
                payload = response.get("Payload").read()
                data = json.loads(payload).get("body", {})
                return data
            else:
                # log to Cloudwatch
                print(f"Request failed: StatusCode {status_code} Error: {data}")
                return {}
        except Exception as ex:
            # log to Cloudwatch
            print(ex)
            return {}
