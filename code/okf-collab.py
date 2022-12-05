from pathlib import Path
import shutil
from mkdocs.commands import build
from mkdocs import config as mkdocs_config
import click
import yaml
from helpers import (
    get_lang_setting,
    get_list_setting,
    update_md_files
)


BASE_CONFIG_FILE = 'base.yml'
CUSTOM_CONFIG_FILE = 'custom.yml'
BASE_FOLDER = Path(__file__).resolve().parent.parent
BASE_CONFIG_FOLDER = Path(BASE_FOLDER) / 'conf'
BASE_PAGE_FOLDER = Path(BASE_FOLDER) / 'page'


@click.group()
def cli():
    pass


@cli.command(
    'build-config',
    short_help='Build config files for all languages'
)
def build_config():
    """ Build the config file """
    base_config = yaml.safe_load(open(BASE_CONFIG_FOLDER / BASE_CONFIG_FILE))
    custom_config = yaml.safe_load(open(BASE_CONFIG_FOLDER / CUSTOM_CONFIG_FILE))

    # Detect languages to prepare final custom mkdocs
    languages = custom_config['site_name'].keys()
    click.echo(f'Languages found: {", ".join(languages)}')
    for language in languages:
        # get the base setting
        config = base_config.copy()

        # take lang-specific settings
        config['copyright'] = get_lang_setting(base_config, language, 'copyright')
        config['theme']['language'] = language
        search_plugin = get_list_setting(config['plugins'], 'search')
        search_plugin['lang'] = language
        wpdf_plugin = get_list_setting(config['plugins'], 'with-pdf')
        wpdf_plugin['output_path'] = f"pdf/doc-{language}.pdf"

        # Override custom settings
        config.update(custom_config)
        config['site_name'] = get_lang_setting(custom_config, language, 'site_name')
        config['site_description'] = get_lang_setting(custom_config, language, 'site_description')
        config['site_author'] = get_lang_setting(custom_config, language, 'site_author')
        config['nav'] = custom_config['nav'][f'nav-{language}']

        config['docs_dir'] = f"../page/docs/docs-{language}"
        if language == 'en':
            config['site_dir'] = f"../site"
        else:
            config['site_dir'] = f"../site/{language}"

        wpdf_plugin['cover_title'] = config['site_name']
        wpdf_plugin['cover_subtitle'] = config['site_description']
        wpdf_plugin['author'] = config['site_author']

        # Update extra values (our context values for all md and html files)
        config['extra'].update(custom_config['custom_extra'])
        # Update MD files with extra values
        click.echo(f'Update docs folder: {config["docs_dir"]}')
        fixed_folder = update_md_files(config['docs_dir'], BASE_CONFIG_FOLDER, context=config['extra'])
        config['docs_dir'] = fixed_folder

        # write the final config file
        final_config_file = BASE_CONFIG_FOLDER / f'mkdocs-{language}.yml'
        with open(final_config_file, 'w') as f:
            yaml.dump(config, f)
        click.echo(f'Config file written to {final_config_file}')

@cli.command(
    'build-site',
    short_help='Build static site and PDFs for all languages'
)
def build_site():
    """ Build the site """
    custom_config = yaml.safe_load(open(BASE_CONFIG_FOLDER / CUSTOM_CONFIG_FILE))
    languages = custom_config['site_name'].keys()

    c = 0
    for language in languages:
        config_file = BASE_CONFIG_FOLDER / f'mkdocs-{language}.yml'
        c += 1
        dirty = c>1
        click.echo(f'Building site for {language} (dirty:{dirty})')
        config = mkdocs_config.load_config(config_file=open(config_file))
        build.build(config, dirty=dirty)
        # copy assets
        src_folder = Path(BASE_PAGE_FOLDER) / 'assets'
        site_dir = config['site_dir']
        dst_folder = Path(site_dir) / 'assets'
        click.echo(f'Copying assets from {src_folder}  to {dst_folder}')
        shutil.copytree(src_folder, dst_folder, dirs_exist_ok=True)

@cli.command(
    'serve',
    short_help='Serve static site'
)
def serve():
    import http.server
    import socketserver

    PORT = 8033
    DIRECTORY = "site"
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)


    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"serving at http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == '__main__':
    cli()
