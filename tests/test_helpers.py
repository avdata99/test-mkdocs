import pytest
from unittest.mock import mock_open, patch
from helpers import (
    get_lang_setting,
    get_list_setting,
    update_gh_action_language_files,
    update_language_paths,
)


def test_get_lang_setting():
    """ Get the language-specific setting from the config dict """

    cfg_dict = {
        'some_key': {
            'fr': 'some value',
        }
    }
    assert get_lang_setting(cfg_dict, 'fr', 'some_key') == 'some value'

    with pytest.raises(ValueError) as e:
        get_lang_setting(cfg_dict, 'fr', 'invalid_key')
    assert str(e.value) == 'Key "invalid_key" not found in config dict'

    with pytest.raises(ValueError) as e:
        get_lang_setting(cfg_dict, 'es', 'some_key')
    assert str(e.value) == 'Language "es" not found for setting "some_key" in config'


def test_get_list_setting():

    cfg_list = [{'set1': {'k10': 'v10', 'k11': 'v11'}}, {'set2': {'k20': 'v20', 'k21': 'v21'}}]
    key = 'set2'
    assert get_list_setting(cfg_list, key) == {'k20': 'v20', 'k21': 'v21'}


def test_update_language_paths_local():
    config = {
        'public_url_base_path': '/some-path',
        'custom_extra': {
            'alternate': [
                {'lang': 'en', 'name': 'English'},
                {'lang': 'fr', 'name': 'Français'},
                {'lang': 'es', 'name': 'Español'},
            ]
        }
    }
    env = 'local'
    update_language_paths(config, env)
    assert config['custom_extra']['alternate'] == [
        {'lang': 'en', 'link': '/', 'name': 'English'},
        {'lang': 'fr', 'link': '/fr', 'name': 'Français'},
        {'lang': 'es', 'link': '/es', 'name': 'Español'},
    ]


def test_update_language_paths_prod():
    config = {
        'public_url_base_path': '/some-path',
        'custom_extra': {
            'alternate': [
                {'lang': 'en', 'name': 'English'},
                {'lang': 'fr', 'name': 'Français'},
                {'lang': 'es', 'name': 'Español'},
            ]
        }
    }
    env = 'prod'
    update_language_paths(config, env)
    assert config['custom_extra']['alternate'] == [
        {'lang': 'en', 'link': '/some-path/', 'name': 'English'},
        {'lang': 'fr', 'link': '/some-path/fr', 'name': 'Français'},
        {'lang': 'es', 'link': '/some-path/es', 'name': 'Español'},
    ]


def test_update_gh_action_language_files():
    gh_workflow_file_path = 'fake-file.yml'
    langs = ['es', 'en', 'pt']
    lines = [
        'pre-text',
        '          # Automatically updated, commit and do not change',
        '          CONFIG_FILES: conf/mkdocs-en.yml conf/mkdocs-es.yml',
        'post-text', ''
    ]
    # We expect the new lang and en lang at the end
    expected_lines = [
        'pre-text',
        '          # Automatically updated, commit and do not change',
        '          CONFIG_FILES: conf/mkdocs-es.yml conf/mkdocs-pt.yml conf/mkdocs-en.yml',
        'post-text',
    ]
    mopen = mock_open(read_data='\n'.join(lines))
    with patch('helpers.open', mopen):
        update_gh_action_language_files(gh_workflow_file_path, langs)
        # mopen.assert_called_with(gh_workflow_file_path, 'r')
        # mopen.assert_called_with(gh_workflow_file_path, 'w')
        handle = mopen()
        # check all langs and order
        handle.writelines.assert_called_once_with(
            [el + '\n' for el in expected_lines]
        )
