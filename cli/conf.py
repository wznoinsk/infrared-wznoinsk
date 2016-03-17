import ConfigParser
import os

import clg

from cli import exceptions
from cli import utils
from cli import logger
from cli.spec import cfg_file_to_dict

LOG = logger.LOG
DEFAULT_CONF_DIRS = dict(
    settings='settings',
    modules='library',
    roles='roles',
    playbooks='playbooks'
)


def load_config_file():
    """Load config file order(ENV, CWD, USER HOME, SYSTEM).

    :return ConfigParser: config object
    """

    # create a parser with default path to InfraRed's main dir
    cwd_path = os.path.join(os.getcwd(), utils.IR_CONF_FILE)
    _config = ConfigParser.ConfigParser()

    env_path = os.getenv(utils.ENV_VAR_NAME, None)
    if env_path is not None:
        env_path = os.path.expanduser(env_path)
        if os.path.isdir(env_path):
            env_path = os.path.join(env_path, utils.IR_CONF_FILE)

    for path in (env_path, cwd_path, utils.USER_PATH, utils.SYSTEM_PATH):
        if path is not None and os.path.exists(path):
            _config.read(path)
            break
    else:
        LOG.warning("Configuration file not found, using InfraRed project dir")
        from os.path import dirname
        project_dir = dirname(dirname(__file__))

        _config.add_section('defaults')
        for option, value in DEFAULT_CONF_DIRS.iteritems():
            _config.set('defaults', option, os.path.join(project_dir, value))

    return _config


config = load_config_file()

# update clg types
clg.TYPES.update({'IniFile': cfg_file_to_dict})
