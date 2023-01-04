from pathlib import Path
from run import (
    BASE_FOLDER,
    get_paths,
)
from helpers_test import (
    build_overrided,
    get_cfg_chuks,
)


PATHS = get_paths(BASE_FOLDER)


def test_add_new_lang_err_missing_site_name():
    """ Test fail adding new language """

    cfg_chunks = get_cfg_chuks()
    override = dict(
        **cfg_chunks['custom_extra_en_es_pt'],
        **cfg_chunks['site_name_en_es'],
    )
    print(f'OVERRIDE\n{override}')
    result = build_overrided(PATHS, override_custom=override)
    assert result.exit_code == 1
    assert 'Languages in site_name and alternate do not match' in result.exception.args[0]
    assert "['en', 'es'] != ['en', 'es', 'pt']" in result.exception.args[0]


def test_add_new_lang_err_missing_alternate():
    """ Test fail adding new language """

    cfg_chunks = get_cfg_chuks()
    override = dict(
        **cfg_chunks['custom_extra_en_es'],
        **cfg_chunks['site_name_en_es_pt'],
    )

    result = build_overrided(PATHS, override_custom=override)
    assert result.exit_code == 1
    assert 'Languages in site_name and alternate do not match' in result.exception.args[0]
    assert "['en', 'es', 'pt'] != ['en', 'es']" in result.exception.args[0]


def test_add_new_lang_err_missing_lang_copyright():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    cfg_chunks = get_cfg_chuks()
    override = dict(
        **cfg_chunks['custom_extra_en_es_pt'],
        **cfg_chunks['site_name_en_es_pt'],
        **cfg_chunks['copyright_en_es'],
    )

    result = build_overrided(PATHS, override_custom=override)
    assert result.exit_code == 1
    assert 'Language "pt" not found for setting "copyright" in config' in result.exception.args[0]


def test_add_new_lang_err_missing_lang_description():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    cfg_chunks = get_cfg_chuks()
    override = dict(
        **cfg_chunks['custom_extra_en_es_pt'],
        **cfg_chunks['site_name_en_es_pt'],
        **cfg_chunks['copyright_en_es_pt'],
        **cfg_chunks['site_description_en_es'],
    )

    result = build_overrided(PATHS, override_custom=override)
    assert result.exit_code == 1
    assert 'Language "pt" not found for setting "site_description" in config' in result.exception.args[0]


def test_add_new_lang_err_missing_lang_site_author():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    cfg_chunks = get_cfg_chuks()
    override = dict(
        **cfg_chunks['custom_extra_en_es_pt'],
        **cfg_chunks['site_name_en_es_pt'],
        **cfg_chunks['copyright_en_es_pt'],
        **cfg_chunks['site_description_en_es_pt'],
        **cfg_chunks['site_author_en_es'],
    )

    result = build_overrided(PATHS, override_custom=override)
    assert result.exit_code == 1
    assert 'Language "pt" not found for setting "site_author" in config' in result.exception.args[0]


def test_add_new_lang_err_missing_lang_nav():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    cfg_chunks = get_cfg_chuks()
    override = dict(
        **cfg_chunks['custom_extra_en_es_pt'],
        **cfg_chunks['site_name_en_es_pt'],
        **cfg_chunks['copyright_en_es_pt'],
        **cfg_chunks['site_description_en_es_pt'],
        **cfg_chunks['site_author_en_es_pt'],
    )

    result = build_overrided(PATHS, override_custom=override)
    assert result.exit_code == 1
    assert 'No "nav-pt" sub-section found in the "nav" section from your custom config file' in result.exception.args[0]


def test_add_new_lang_err_missing_lang_nav_index():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    cfg_chunks = get_cfg_chuks()
    override = dict(
        **cfg_chunks['custom_extra_en_es_pt'],
        **cfg_chunks['site_name_en_es_pt'],
        **cfg_chunks['copyright_en_es_pt'],
        **cfg_chunks['site_description_en_es_pt'],
        **cfg_chunks['site_author_en_es_pt'],
        **cfg_chunks['nav_en_es_pt_no_index'],
    )

    result = build_overrided(PATHS, override_custom=override)
    assert result.exit_code == 1
    assert 'No "index.md" found in the "nav-pt" sub-section from your custom config file' in result.exception.args[0]


def test_add_new_lang_err_missing_lang_docs_folder():
    """ Test fail adding new language """

    # Override site names and alternates with PT
    cfg_chunks = get_cfg_chuks()
    override = dict(
        **cfg_chunks['custom_extra_en_es_pt'],
        **cfg_chunks['site_name_en_es_pt'],
        **cfg_chunks['copyright_en_es_pt'],
        **cfg_chunks['site_description_en_es_pt'],
        **cfg_chunks['site_author_en_es_pt'],
        **cfg_chunks['nav_en_es_pt'],
    )

    result = build_overrided(PATHS, override_custom=override)
    assert result.exit_code == 1
    assert 'Docs folder not found' in result.exception.args[0]
    assert '/docs/docs-pt' in result.exception.args[0]


def test_add_new_lang_OK():
    """ Test OK adding new language """

    cfg_chunks = get_cfg_chuks()
    override = dict(
        **cfg_chunks['custom_extra_en_es_pt'],
        **cfg_chunks['site_name_en_es_pt'],
        **cfg_chunks['copyright_en_es_pt'],
        **cfg_chunks['site_description_en_es_pt'],
        **cfg_chunks['site_author_en_es_pt'],
        **cfg_chunks['nav_en_es_pt'],
    )

    docs_test_folder = '../test-folder'
    override_base = {
        'docs_dir': docs_test_folder,
    }

    # Create a test folder will all language index files
    Path(docs_test_folder).mkdir(exist_ok=True)
    Path(docs_test_folder + '/docs-en').mkdir(exist_ok=True)
    Path(docs_test_folder + '/docs-en/index.md').touch()
    Path(docs_test_folder + '/docs-es').mkdir(exist_ok=True)
    Path(docs_test_folder + '/docs-es/index.md').touch()
    Path(docs_test_folder + '/docs-pt').mkdir(exist_ok=True)
    Path(docs_test_folder + '/docs-pt/index.md').touch()

    result = build_overrided(PATHS, override_custom=override, override_base=override_base)

    assert result.exit_code == 0
