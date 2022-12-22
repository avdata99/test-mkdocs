import builtins
import os
from pathlib import Path
# from unittest import TestCase
from unittest.mock import mock_open, patch
from click.testing import CliRunner
import pytest
from run import (
    BASE_FOLDER,
    build_config,
    get_paths,
)

PATHS = get_paths(BASE_FOLDER)


bad_yaml_lines = [
    'bad-values:',
    '  - some-list: a',
    '  some-dict-mixed: b',

]
bad_yaml_content = '\n'.join(bad_yaml_lines)


def _side_path_exists(path_not_exists):
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


def _side_open_read(path, result):
    """ Return a side_effect function for open to
        return "result" on path and real value on other paths
    """
    original_open_fn = open
    def side_effect(*args, **kwargs):
        is_read = len(args) == 1 or args[1] == 'r'
        if not is_read:
            return original_open_fn(*args, **kwargs)
        if args[0] == path:
            return result
        else:
            return original_open_fn(*args, **kwargs)

    return side_effect


@pytest.mark.parametrize("path", [PATHS['base_config_file'], PATHS['custom_config_file']])
def test_build_cfg_err_no_cfg(path):
    """ test base_config_file do not exists """

    side_effect = _side_path_exists(path)
    with patch('helpers.os.path.exists') as path_exists:
        path_exists.side_effect = side_effect

        runner = CliRunner()
        result = runner.invoke(build_config, ['--env=local'])
        assert result.exit_code == 1
        assert 'YAML file does not exist' in result.exception.args[0]
        assert str(path) in result.exception.args[0]


def test_build_cfg_err_no_custom_cfg():
    """ test custom_config_file do not exists """

    side_effect = _side_path_exists(PATHS['custom_config_file'])
    with patch('helpers.os.path.exists') as path_exists:
        path_exists.side_effect = side_effect

        runner = CliRunner()
        result = runner.invoke(build_config, ['--env=local'])
        assert result.exit_code == 1
        if result.exception:
            import traceback
            traceback.print_exception(*result.exc_info)
        assert 'YAML file does not exist' in result.exception.args[0]
        assert str(PATHS['custom_config_file']) in result.exception.args[0]


@pytest.mark.parametrize("path", [PATHS['base_config_file'], PATHS['custom_config_file']])
def test_build_cfg_err_bad_yaml(path):
    """ test base_config_file is not valid YAML """
    side_effect = _side_open_read(path, bad_yaml_content)
    with patch('helpers.open') as mock_open:
        mock_open.side_effect = side_effect
        runner = CliRunner()
        result = runner.invoke(build_config, ['--env=local'])
        assert result.exit_code == 1
        if result.exception:
            import traceback
            traceback.print_exception(*result.exc_info)

        assert 'YAML file is not valid YAML' in result.exception.args[0]
        assert str(path) in result.exception.args[0]
