import os
from unittest.mock import patch
from click.testing import CliRunner
from helpers import get_yaml
from run import build_config


bad_yaml_lines = [
    'bad-values:',
    '  - some-list: a',
    '  some-dict-mixed: b',

]
bad_yaml_content = '\n'.join(bad_yaml_lines)


def side_path_exists(path_not_exists):
    """ Return a side_effect function for os.path.exists to
        return False on path_not_exists and real value on other paths
    """
    original_exists_fn = os.path.exists

    def side_effect(*args, **kwargs):
        if args[0] == path_not_exists:
            return False
        else:
            return original_exists_fn(*args, **kwargs)

    return side_effect


def side_open_read(path, result=None, replace_path=None):
    """ Return a side_effect function for open to
        return "result" on path and real value on other paths
    """
    original_open_fn = open

    def side_effect(*args, **kwargs):
        is_read = len(args) == 1 or args[1] == 'r'
        if not is_read:
            return original_open_fn(*args, **kwargs)
        if args[0] == path:
            if result:
                return result
            elif replace_path:
                return original_open_fn(replace_path, 'r', **kwargs)
        else:
            return original_open_fn(*args, **kwargs)

    return side_effect


def get_yaml_and_override(path, overrides):
    orig_get_yaml = get_yaml

    def side_effect(*args, **kwargs):
        base = orig_get_yaml(*args, **kwargs)
        if args[0] == path:
            base.update(overrides)
        return base

    return side_effect


def build_overrided(overrides, PATHS):
    """ Run the build process overriding the custom config file
        and return a mocked get_yaml function to read results """
    side_effect = get_yaml_and_override(PATHS['custom_config_file'], overrides)
    with patch('run.get_yaml') as get_yaml:
        get_yaml.side_effect = side_effect
        runner = CliRunner()
        result = runner.invoke(build_config, ['--env=local'])
        assert result.exit_code == 0

    return get_yaml
