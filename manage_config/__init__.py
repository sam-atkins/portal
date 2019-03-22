import os

import anyconfig


class Config():
    conf = {}

    @classmethod
    def make(self):
        anyconfig.merge(self.conf, os.environ.copy())
        stage = self.conf.get('stage', None)
        project_config_dir = self.conf.get('project_config_dir', None)

        project_default_config_file_path = os.path.join(
            project_config_dir, 'default.yml')
        if os.path.exists(project_default_config_file_path):
            anyconfig.merge(self.conf,
                            anyconfig.load(project_default_config_file_path))

        project_stage_config_file_path = os.path.join(project_config_dir,
                                                      f'{stage}.yml')
        if os.path.exists(project_stage_config_file_path):
            anyconfig.merge(self.conf,
                            anyconfig.load(project_stage_config_file_path))


def get_config(key_name, default=None):
    return Config.conf.get(key_name, default)


def make_settings():
    Config.make()


make_settings()
