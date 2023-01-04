import copy
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


def side_path_exists(path, ret_value=False):
    """ Return a side_effect function for os.path.exists to
        return Boolean on path and real value on other paths
    """
    original_exists_fn = os.path.exists

    def side_effect(*args, **kwargs):
        if args[0] == path:
            return ret_value
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


def get_yaml_and_override(overrides):
    """ Return a side_effect function for get_yaml to
        return the original get_yaml result and override
        the result for the given path
        overrides: dict with key=path and value=dict to override the yaml result
    """
    orig_get_yaml = get_yaml

    def side_effect(*args, **kwargs):
        base = orig_get_yaml(*args, **kwargs)
        if args[0] in overrides.keys():
            base.update(overrides[args[0]])
        return base

    return side_effect


def build_overrided(
    PATHS,
    override_base={},
    override_custom={},
    extra_build_params=['--skip-gh-action'],
    env='local'
):
    """ Run the build process overriding the custom config file
        and returns the result of the build process """

    overrides = {
        PATHS['custom_config_file']: override_custom,
        PATHS['base_config_file']: override_base
    }
    side_effect = get_yaml_and_override(overrides)

    with patch('run.get_yaml') as get_yaml:
        get_yaml.side_effect = side_effect
        runner = CliRunner()
        result = runner.invoke(build_config, [f'--env={env}'] + extra_build_params)
        if result.exception:
            import traceback
            traceback.print_exception(*result.exc_info)
        return result


def get_cfg_chuks():

    custom_extra_en_es = {
        'custom_extra': {
            'alternate': [
                {'name': 'English', 'lang': 'en'},
                {'name': 'Español', 'lang': 'es'},
            ],
            'test_var': '',
            'test_complex_obj': {'test_var2': '', 'test_var3': ''},
        }
    }
    custom_extra_en_es_pt = copy.deepcopy(custom_extra_en_es)
    custom_extra_en_es_pt['custom_extra']['alternate'].append(
        {'name': 'Português', 'lang': 'pt'}
    )

    site_name_en_es = {
        'site_name': {
            'en': 'Collab test',
            'es': 'Mi test',
        }
    }
    site_name_en_es_pt = copy.deepcopy(site_name_en_es)
    site_name_en_es_pt['site_name']['pt'] = 'Meu teste'

    copyright_en_es = {
        'copyright': {
            'en': 'Copyrigth',
            'es': 'Derechos de autor',
        }
    }
    copyright_en_es_pt = copy.deepcopy(copyright_en_es)
    copyright_en_es_pt['copyright']['pt'] = 'Copyrigth'

    site_description_en_es = {
        'site_description': {
            'en': 'Descr',
            'es': 'Descr',
        }
    }
    site_description_en_es_pt = copy.deepcopy(site_description_en_es)
    site_description_en_es_pt['site_description']['pt'] = 'Descr'

    site_author_en_es = {
        'site_author': {
            'en': 'Author',
            'es': 'Author',
        }
    }
    site_author_en_es_pt = copy.deepcopy(site_author_en_es)
    site_author_en_es_pt['site_author']['pt'] = 'Author'

    nav_en_es = {
        'nav': {
            'nav-en': [{'Home': 'index.md'}],
            'nav-es': [{'Inicio': 'index.md'}],
        }
    }
    nav_en_es_pt_no_index = copy.deepcopy(nav_en_es)
    nav_en_es_pt_no_index['nav']['nav-pt'] = [{'Início': 'bad-index.md'}]

    nav_en_es_pt = copy.deepcopy(nav_en_es)
    nav_en_es_pt['nav']['nav-pt'] = [{'Início': 'index.md'}]

    return {
        'custom_extra_en_es': custom_extra_en_es,
        'custom_extra_en_es_pt': custom_extra_en_es_pt,
        'site_name_en_es': site_name_en_es,
        'site_name_en_es_pt': site_name_en_es_pt,
        'copyright_en_es': copyright_en_es,
        'copyright_en_es_pt': copyright_en_es_pt,
        'site_description_en_es': site_description_en_es,
        'site_description_en_es_pt': site_description_en_es_pt,
        'site_author_en_es': site_author_en_es,
        'site_author_en_es_pt': site_author_en_es_pt,
        'nav_en_es': nav_en_es,
        'nav_en_es_pt': nav_en_es_pt,
        'nav_en_es_pt_no_index': nav_en_es_pt_no_index,
    }
