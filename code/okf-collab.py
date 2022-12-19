from pathlib import Path
import shutil
from mkdocs.commands import build
from mkdocs import config as mkdocs_config
import click
import yaml
from helpers import (
    get_lang_setting,
    get_list_setting,
    update_language_paths,
    update_md_files,
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
@click.option('--env', '-e', default='local', help='Environment to build for (local or prod)')
def build_config(env):
    """ Build the config file """
    base_config = yaml.safe_load(open(BASE_CONFIG_FOLDER / BASE_CONFIG_FILE))
    custom_config = yaml.safe_load(open(BASE_CONFIG_FOLDER / CUSTOM_CONFIG_FILE))

    # Define all language final paths
    update_language_paths(custom_config, env)

    # Changes for prod env
    if env == 'prod':
        # Prod env can use custom base path for URLs, locally is not required
        base_config['extra']['assets_folder'] = custom_config['public_url_base_path'] + base_config['extra']['assets_folder']

    # Copy general assets (for all languages).
    src_folder = Path(BASE_PAGE_FOLDER) / 'assets'
    dst_folder = Path(BASE_FOLDER) / 'site' / 'assets'
    click.echo(f'Copying assets from {src_folder}  to {dst_folder}')
    shutil.copytree(src_folder, dst_folder, dirs_exist_ok=True)

    # Detect languages to prepare final custom mkdocs
    languages = custom_config['site_name'].keys()
    click.echo(f'Languages found: {", ".join(languages)}')
    for language in languages:
        # get the base setting
        config = base_config.copy()

        config['theme']['language'] = language
        search_plugin = get_list_setting(config['plugins'], 'search')
        search_plugin['lang'] = language
        wpdf_plugin = get_list_setting(config['plugins'], 'with-pdf')
        wpdf_plugin['output_path'] = f"pdf/doc-{language}.pdf"

        # Override custom settings
        config.update(custom_config)
        config['copyright'] = get_lang_setting(custom_config, language, 'copyright')
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

        # fix CSS and JS statics
        final_css = []
        for css in config['extra_css']:
            if css.startswith('/'):
                css = config['extra']['assets_folder'] + css
            final_css.append(css)
        config['extra_css'] = final_css

        final_js = []
        for js in config['extra_javascript']:
            if js.startswith('/'):
                js = config['extra']['assets_folder'] + js
            final_js.append(js)
        config['extra_javascript'] = final_js

        # Update extra values (our context values for all md and html files)
        config['extra'].update(custom_config['custom_extra'])
        # Update MD files with extra values
        click.echo(f'Update docs folder: {config["docs_dir"]}')
        fixed_folder = update_md_files(config['docs_dir'], BASE_CONFIG_FOLDER, context=config['extra'])
        config['docs_dir'] = fixed_folder

        # Remove configurations not recognized by mkdocs
        config.pop('public_url_base_path', None)
        config.pop('custom_extra', None)

        # write the final config file
        final_config_file = BASE_CONFIG_FOLDER / f'mkdocs-{language}.yml'
        with open(final_config_file, 'w') as f:
            yaml.dump(config, f)
        click.echo(f'Config file written to {final_config_file}')


@cli.command(
    'build-local-site',
    short_help='Build static site to run locally'
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

    # Copy general assets (same for all languages).
    src_folder = Path(BASE_PAGE_FOLDER) / 'assets'
    dst_folder = Path(BASE_FOLDER) / 'site' / 'assets'
    click.echo(f'Copying assets from {src_folder}  to {dst_folder}')
    shutil.copytree(src_folder, dst_folder, dirs_exist_ok=True)


@cli.command(
    'serve',
    short_help='Serve static site'
)
@click.option('--port', '-p', default=8033, type=click.INT, help='Port for the test local erver')
def serve(port):
    import http.server
    import socketserver

    DIRECTORY = "site"
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)


    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"serving at http://localhost:{port}")
        httpd.serve_forever()


if __name__ == '__main__':
    cli()
