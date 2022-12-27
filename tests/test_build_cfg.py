from unittest.mock import patch
from click.testing import CliRunner
import pytest
from run import (
    BASE_FOLDER,
    build_config,
    get_paths,
)
from helpers_test import (
    bad_yaml_content,
    get_yaml_and_override,
    side_path_exists,
    side_open_read,
)


PATHS = get_paths(BASE_FOLDER)


@pytest.mark.parametrize("path", [PATHS['base_config_file'], PATHS['custom_config_file']])
def test_build_cfg_err_no_cfg(path):
    """ test base_config_file do not exists """

    side_effect = side_path_exists(path)
    with patch('helpers.os.path.exists') as path_exists:
        path_exists.side_effect = side_effect

        runner = CliRunner()
        result = runner.invoke(build_config, ['--env=local'])
        assert result.exit_code == 1
        assert 'YAML file does not exist' in result.exception.args[0]
        assert str(path) in result.exception.args[0]


def test_build_cfg_err_no_custom_cfg():
    """ test custom_config_file do not exists """

    side_effect = side_path_exists(PATHS['custom_config_file'])
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
    side_effect = side_open_read(path, bad_yaml_content)
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


def test_custom_site_url():
    """ test custom site urls """
    overrides = {
        'custom_site_url': 'http://custom-site-url.com',
    }

    side_effect = get_yaml_and_override(PATHS['custom_config_file'], overrides)
    with patch('run.get_yaml') as get_yaml:
        get_yaml.side_effect = side_effect
        runner = CliRunner()
        result = runner.invoke(build_config, ['--env=local'])
        assert result.exit_code == 0

    # check output
    final_config_files = [
        PATHS['base_config_folder'] / 'mkdocs-en.yml',
        PATHS['base_config_folder'] / 'mkdocs-es.yml',
    ]
    for final_config_file in final_config_files:
        res = get_yaml(final_config_file)
        assert res['site_url'] == overrides['custom_site_url']


def test_gh_site_url():
    """ test github urls """
    overrides = {
        'repo_name': 'repo',
        'repo_user': 'user',
    }

    side_effect = get_yaml_and_override(PATHS['custom_config_file'], overrides)
    with patch('run.get_yaml') as get_yaml:
        get_yaml.side_effect = side_effect
        runner = CliRunner()
        result = runner.invoke(build_config, ['--env=local'])
        assert result.exit_code == 0

    # check output
    final_config_files = [
        PATHS['base_config_folder'] / 'mkdocs-en.yml',
        PATHS['base_config_folder'] / 'mkdocs-es.yml',
    ]
    for final_config_file in final_config_files:
        res = get_yaml(final_config_file)
        assert res['site_url'] == f"https://{overrides['repo_user']}.github.io/{overrides['repo_name']}"
