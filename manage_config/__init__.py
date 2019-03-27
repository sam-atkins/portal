import ast
import json
import os

import anyconfig
import boto3


class Config:
    """Merges in config objects to make one conf object"""

    conf = {}

    def _deserialise(self, name, value):
        """Deserialise JSON values to Python

        Args:
            name (str): the config key name
            value (str): the config value

        Returns:
            value: deserialised config value
        """
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception as ex:
                raise Exception(ex)
        else:
            return value

    def _evaluate(self, name, value):
        """Literal evaluation of a string containing a Python expression

        Args:
            name (str): the config key name
            value (str): the config value

        Returns:
            value: evaluated config value
        """
        if isinstance(value, str):
            try:
                return ast.literal_eval(value)
            except Exception:
                return value
        else:
            return value

    def get_remote_params(self, parameters_path):
        """Fetches remote config from AWS Systems Manager Param Store

        Args:
            parameters_path (str): the path of the params to fetch
                /{project_name}/{stage}/

        Returns:
            dict: remote config
        """
        client = boto3.client("ssm")
        response = {}
        try:
            payload = client.get_parameters_by_path(
                Path=parameters_path, Recursive=True, WithDecryption=True
            )

            remote_params = payload.get("Parameters", [])
            for param in remote_params:
                name = param.get("Name", None)
                name = name.split("/")[-1]
                value = param.get("Value", None)

                deserialised_value = self._deserialise(self, name, value)
                evaluated_value = self._evaluate(self, name, deserialised_value)
                response[name] = evaluated_value
            return response
        except Exception as ex:
            raise Exception from ex

    @classmethod
    def make(self):
        """Makes the conf object, merging in the following order:

            - ENV
            - default config: default.yml
            - stage config: {stage}.yml
            - remote config: remote_settings
        """
        anyconfig.merge(self.conf, os.environ.copy())
        stage = self.conf.get("stage", None)
        project_config_dir = self.conf.get("project_config_dir", None)

        project_default_config_file_path = os.path.join(
            project_config_dir, "default.yml"
        )
        if os.path.exists(project_default_config_file_path):
            anyconfig.merge(self.conf, anyconfig.load(project_default_config_file_path))

        project_stage_config_file_path = os.path.join(
            project_config_dir, f"{stage}.yml"
        )
        if os.path.exists(project_stage_config_file_path):
            anyconfig.merge(self.conf, anyconfig.load(project_stage_config_file_path))
        remote_settings = self.conf.get("use_remote_settings", None)
        if remote_settings:
            project_name = self.conf.get("project_name", None)
            parameters_path = f"/{project_name}/{stage}/"
            remote_conf = self.get_remote_params(self, parameters_path)
            anyconfig.merge(self.conf, remote_conf)


def get_config(key_name, default=None):
    return Config.conf.get(key_name, default)


def make_settings():
    Config.make()


make_settings()