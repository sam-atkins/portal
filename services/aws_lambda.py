"""AWS Lambda invocations to services"""
import json
from typing import Any, Dict

import boto3


class LambdaProxy:
    """Invokes requests to Lambda functions"""

    def invoke_lambda_function(
        self, service_function_name: str, payload: Dict[str, Any]
    ):
        """Invoke a Lambda function

        Args:
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
                response_payload = response.get("Payload").read()
                data = json.loads(response_payload).get("body", {})
                return data
            else:
                # log to Cloudwatch
                print(f"Request failed: StatusCode {status_code} Error: {data}")
                return {}
        except Exception as ex:
            # log to Cloudwatch
            print(ex)
            return {}
