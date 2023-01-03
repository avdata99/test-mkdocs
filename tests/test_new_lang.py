from pathlib import Path
from run import (
    BASE_FOLDER,
    get_paths,
)
from helpers_test import (
    build_overrided,
)


PATHS = get_paths(BASE_FOLDER)
custom_new_lang_alternate = {
    'custom_extra': {
        'alternate': [
            {'name': 'English', 'lang': 'en'},
            {'name': 'Español', 'lang': 'es'},
            {'name': 'Português', 'lang': 'pt'},
        ],
        'test_var': '',
        'test_complex_obj': {'test_var2': '', 'test_var3': ''},
    },
}


def test_add_new_lang_err_missing_site_name():
    """ Test fail adding new language """

    result = build_overrided(PATHS, override_custom=custom_new_lang_alternate)
    assert result.exit_code == 1
    assert 'Languages in site_name and alternate do not match' in result.exception.args[0]
    assert "['en', 'es'] != ['en', 'es', 'pt']" in result.exception.args[0]


def test_add_new_lang_err_missing_alternate():
    """ Test fail adding new language """

    overrides = {
        'site_name': {
            'en': 'My site name',
            'es': 'Mi sitio',
            'pt': 'Meu site',
        }
    }

    result = build_overrided(PATHS, override_custom=overrides)
    assert result.exit_code == 1
    assert 'Languages in site_name and alternate do not match' in result.exception.args[0]
    assert "['en', 'es', 'pt'] != ['en', 'es']" in result.exception.args[0]


def test_add_new_lang_err_missing_lang_copyright():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    overrides = {
        'site_name': {
            'en': 'My site name',
            'es': 'Mi sitio',
            'pt': 'Meu site',
        }
    }
    overrides.update(custom_new_lang_alternate)

    result = build_overrided(PATHS, override_custom=overrides)
    assert result.exit_code == 1
    assert 'Language "pt" not found for setting "copyright" in config' in result.exception.args[0]


def test_add_new_lang_err_missing_lang_description():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    overrides = {
        'site_name': {
            'en': 'My site name',
            'es': 'Mi sitio',
            'pt': 'Meu site',
        },
        'copyright': {
            'en': 'Copyrigth',
            'es': 'Copyrigth',
            'pt': 'Copyrigth',
        }
    }
    overrides.update(custom_new_lang_alternate)

    result = build_overrided(PATHS, override_custom=overrides)
    assert result.exit_code == 1
    assert 'Language "pt" not found for setting "site_description" in config' in result.exception.args[0]


def test_add_new_lang_err_missing_lang_site_author():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    overrides = {
        'site_name': {
            'en': 'My site name',
            'es': 'Mi sitio',
            'pt': 'Meu site',
        },
        'copyright': {
            'en': 'Copyrigth',
            'es': 'Copyrigth',
            'pt': 'Copyrigth',
        },
        'site_description': {
            'en': 'Copyrigth',
            'es': 'Copyrigth',
            'pt': 'Copyrigth',
        }
    }
    overrides.update(custom_new_lang_alternate)

    result = build_overrided(PATHS, override_custom=overrides)
    assert result.exit_code == 1
    assert 'Language "pt" not found for setting "site_author" in config' in result.exception.args[0]


def test_add_new_lang_err_missing_lang_nav():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    overrides = {
        'site_name': {
            'en': 'My site name',
            'es': 'Mi sitio',
            'pt': 'Meu site',
        },
        'copyright': {
            'en': 'Copyrigth',
            'es': 'Copyrigth',
            'pt': 'Copyrigth',
        },
        'site_description': {
            'en': 'description',
            'es': 'description',
            'pt': 'description',
        },
        'site_author': {
            'en': 'author',
            'es': 'author',
            'pt': 'author',
        }
    }
    overrides.update(custom_new_lang_alternate)

    result = build_overrided(PATHS, override_custom=overrides)
    assert result.exit_code == 1
    assert 'No "nav-pt" sub-section found in the "nav" section from your custom config file' in result.exception.args[0]


def test_add_new_lang_err_missing_lang_nav_index():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    overrides = {
        'site_name': {
            'en': 'My site name',
            'es': 'Mi sitio',
            'pt': 'Meu site',
        },
        'copyright': {
            'en': 'Copyrigth',
            'es': 'Copyrigth',
            'pt': 'Copyrigth',
        },
        'site_description': {
            'en': 'description',
            'es': 'description',
            'pt': 'description',
        },
        'site_author': {
            'en': 'author',
            'es': 'author',
            'pt': 'author',
        },
        'nav': {
            'nav-en': [{'Home': 'index.md'}],
            'nav-es': [{'Inicio': 'index.md'}],
            # at leat one index.md is required
            'nav-pt': [{'Inicio': 'no-index.md'}],
        }
    }

    overrides.update(custom_new_lang_alternate)

    result = build_overrided(PATHS, override_custom=overrides)
    assert result.exit_code == 1
    assert 'No "index.md" found in the "nav-pt" sub-section from your custom config file' in result.exception.args[0]


def test_add_new_lang_err_missing_lang_docs_folder():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    overrides = {
        'site_name': {
            'en': 'My site name',
            'es': 'Mi sitio',
            'pt': 'Meu site',
        },
        'copyright': {
            'en': 'Copyrigth',
            'es': 'Copyrigth',
            'pt': 'Copyrigth',
        },
        'site_description': {
            'en': 'description',
            'es': 'description',
            'pt': 'description',
        },
        'site_author': {
            'en': 'author',
            'es': 'author',
            'pt': 'author',
        },
        'nav': {
            'nav-en': [{'Home': 'index.md'}],
            'nav-es': [{'Inicio': 'index.md'}],
            'nav-pt': [{'Inicio': 'index.md'}],
        }
    }

    overrides.update(custom_new_lang_alternate)

    result = build_overrided(PATHS, override_custom=overrides)
    assert result.exit_code == 1
    assert 'Docs folder not found' in result.exception.args[0]
    assert '/docs/docs-pt' in result.exception.args[0]


def test_add_new_lang_OK():
    """ Test OK adding new language """

    override_custom = {
        'site_name': {
            'en': 'My site name',
            'es': 'Mi sitio',
            'pt': 'Meu site',
        },
        'copyright': {
            'en': 'Copyrigth',
            'es': 'Copyrigth',
            'pt': 'Copyrigth',
        },
        'site_description': {
            'en': 'description',
            'es': 'description',
            'pt': 'description',
        },
        'site_author': {
            'en': 'author',
            'es': 'author',
            'pt': 'author',
        },
        'nav': {
            'nav-en': [{'Home': 'index.md'}],
            'nav-es': [{'Inicio': 'index.md'}],
            'nav-pt': [{'Inicio': 'index.md'}],
        },
    }

    docs_test_folder = '../test-folder'
    override_base = {
        'docs_dir': docs_test_folder,
    }

    override_custom.update(custom_new_lang_alternate)

    # Create a test folder will all language index files
    Path(docs_test_folder).mkdir(exist_ok=True)
    Path(docs_test_folder + '/docs-en').mkdir(exist_ok=True)
    Path(docs_test_folder + '/docs-en/index.md').touch()
    Path(docs_test_folder + '/docs-es').mkdir(exist_ok=True)
    Path(docs_test_folder + '/docs-es/index.md').touch()
    Path(docs_test_folder + '/docs-pt').mkdir(exist_ok=True)
    Path(docs_test_folder + '/docs-pt/index.md').touch()

    result = build_overrided(PATHS, override_custom=override_custom, override_base=override_base)

    assert result.exit_code == 0
