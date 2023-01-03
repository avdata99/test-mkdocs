from run import (
    BASE_FOLDER,
    get_paths,
)
from helpers import get_yaml
from helpers_test import build_overrided


PATHS = get_paths(BASE_FOLDER)


def test_assets_folder():
    """ test assets folder for prod """

    overrides = {
        'repo_name': 'repo',
        'repo_user': 'user',
    }

    results = build_overrided(PATHS, override_custom=overrides, env='prod')
    assert results.exit_code == 0

    # check output
    final_config_files = [
        PATHS['base_config_folder'] / 'mkdocs-en.yml',
        PATHS['base_config_folder'] / 'mkdocs-es.yml',
    ]
    for final_config_file in final_config_files:
        res = get_yaml(final_config_file)
        assert res['extra']['assets_folder'] == '/' + overrides['repo_name'] + '/assets'


def test_lang_urls():
    """ test assets folder for prod """

    overrides = {
        'repo_name': 'repo',
        'repo_user': 'user',
    }

    results = build_overrided(PATHS, override_custom=overrides, env='prod')
    assert results.exit_code == 0

    # check output en
    final_config_files = [
        PATHS['base_config_folder'] / 'mkdocs-en.yml',
        PATHS['base_config_folder'] / 'mkdocs-es.yml',
    ]
    for final_config_file in final_config_files:
        res = get_yaml(final_config_file)
        langs = res['extra']['alternate']
        for lang in langs:
            lang_code = '' if lang['lang'] == 'en' else lang['lang']
            assert lang['link'] == '/' + overrides['repo_name'] + '/' + lang_code
