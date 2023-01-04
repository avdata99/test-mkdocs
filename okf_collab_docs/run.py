from pathlib import Path
import shutil
from mkdocs.commands import build
from mkdocs import config as mkdocs_config
import click
import git
import yaml


from helpers import (
    add_pdf_url,
    get_lang_setting,
    get_list_setting,
    get_paths,
    get_yaml,
    update_gh_action_language_files,
    update_language_paths,
    update_md_files,
    validate_index_lang_file,
    validate_langs,
    validate_nav_lang_exists,
)


BASE_FOLDER = Path(__file__).resolve().parent.parent


@click.group()
def cli():
    pass


@cli.command(
    'build-config',
    short_help='Build config files for all languages'
)
@click.option('--env', '-e', default='local', help='Environment to build for (local or prod)')
@click.option('--skip-gh-action', is_flag=True, help='Skip updating GitHub action file')
def build_config(skip_gh_action, env):
    """ Build the config file """
    PATHS = get_paths(BASE_FOLDER)
    base_config = get_yaml(PATHS['base_config_file'])
    custom_config = get_yaml(PATHS['custom_config_file'])

    # Detect languages to validate and prepare final custom mkdocs
    languages = validate_langs(custom_config)

    # Copy general assets (for all languages).
    src_folder = PATHS['user_assets_folder']
    dst_folder = PATHS['site_assets_folder']
    click.echo(f'Copying assets from {src_folder}  to {dst_folder}')
    shutil.copytree(src_folder, dst_folder, dirs_exist_ok=True)

    # Update the GitHub action to contain the correct language files
    if not skip_gh_action:
        gh_workflow_file_path = PATHS['base_folder'] / '.github/workflows/page.yml'
        click.echo(f'Updating GitHub action file: {gh_workflow_file_path}')
        update_gh_action_language_files(gh_workflow_file_path, languages)

    # ====================
    # URLs
    repo_name = custom_config.pop('repo_name')
    repo_user = custom_config.pop('repo_user')
    custom_config['repo_url'] = f'https://github.com/{repo_user}/{repo_name}'

    if custom_config.get('custom_site_url'):
        custom_config['site_url'] = custom_config['custom_site_url']
        custom_config['public_url_base_path'] = custom_config.get('public_url_base_path', '')
    else:
        custom_config['public_url_base_path'] = f'/{repo_name}'
        custom_config['site_url'] = f'https://{repo_user}.github.io/{repo_name}'

    # Changes for prod env
    if env == 'prod':
        # Prod env can use custom base path for URLs, locally is not required
        pbu = custom_config.get('public_url_base_path', '')
        base_config['extra']['assets_folder'] = pbu + base_config['extra']['assets_folder']

    # Define all language final paths
    update_language_paths(custom_config, env)
    # ====================

    click.echo(f'Languages found: {", ".join(languages)}')
    for language in languages:
        # get the base setting
        config = base_config.copy()
        base_docs_dir = config['docs_dir']

        config['theme']['language'] = language
        search_plugin = get_list_setting(config['plugins'], 'search')
        search_plugin['lang'] = language
        wpdf_plugin = get_list_setting(config['plugins'], 'with-pdf')
        wpdf_plugin['output_path'] = f"pdf/doc-{language}.pdf"

        config['edit_uri'] = base_config['edit_uri'].replace('LANG', language)
        config['docs_dir'] = f"{base_docs_dir}/docs-{language}"

        # Override custom settings
        config.update(custom_config)
        config['copyright'] = get_lang_setting(custom_config, language, 'copyright')
        config['site_name'] = get_lang_setting(custom_config, language, 'site_name')
        config['site_description'] = get_lang_setting(custom_config, language, 'site_description')
        config['site_author'] = get_lang_setting(custom_config, language, 'site_author')
        validate_nav_lang_exists(custom_config['nav'], language)
        config['nav'] = custom_config['nav'][f'nav-{language}']
        # Check for the default index.md (required for all languages)
        validate_index_lang_file(config['nav'], language)

        if language == 'en':
            config['site_dir'] = "../site"
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

        # Add a final PDF URL for this language
        add_pdf_url(config, wpdf_plugin, language)

        # Update MD files with extra values
        click.echo(f'Update docs folder: {config["docs_dir"]}')
        fixed_folder = update_md_files(config['docs_dir'], PATHS['base_config_folder'], context=config['extra'])
        config['docs_dir'] = fixed_folder

        # Remove configurations not recognized by mkdocs
        config.pop('public_url_base_path', None)
        config.pop('custom_extra', None)

        # write the final config file
        final_config_file = PATHS['base_config_folder'] / f'mkdocs-{language}.yml'
        with open(final_config_file, 'w') as f:
            yaml.dump(config, f)
        click.echo(f'Config file written to {final_config_file}')


@cli.command(
    'build-local-site',
    short_help='Build static site to run locally'
)
def build_site():
    """ Build the site """
    PATHS = get_paths(BASE_FOLDER)
    custom_config = yaml.safe_load(open(PATHS['custom_config_file']))
    languages = custom_config['site_name'].keys()

    c = 0
    for language in languages:
        config_file = PATHS['base_config_folder'] / f'mkdocs-{language}.yml'
        c += 1
        dirty = c > 1
        click.echo(f'Building site for {language} (dirty:{dirty})')
        config = mkdocs_config.load_config(config_file=open(config_file))
        build.build(config, dirty=dirty)

    # Copy general assets (same for all languages).
    src_folder = PATHS['user_assets_folder']
    dst_folder = PATHS['site_assets_folder']

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


@cli.command(
    'update-from-template',
    short_help='Get latest changes from upstream template'
)
def update():
    """ Get changes from base template """

    # Local repo on your computer
    repo = git.Repo('.')
    # Create a remote to template upstream repo (if not exists)
    try:
        upstream = repo.create_remote('upstream', 'git@github.com:okfn/okfn-collaborative-docs.git')
    except git.exc.GitCommandError:
        upstream = repo.remote('upstream')
    upstream.fetch()
    cmd = repo.git
    cmd.rebase('-Xours', 'upstream/main')


@cli.command(
    'init',
    short_help='Initialize this project'
)
def init_project():
    """ Initialize basic files and settings """

    # Local repo on your computer
    repo = git.Repo('.')
    remote = repo.remote()
    remote_url = remote.url
    repo_user = remote_url.split('/')[-2].split(':')[1]
    repo_name = remote_url.split('/')[-1].replace('.git', '')

    click.echo(f'Initializing project for {repo_user}/{repo_name}')

    PATHS = get_paths(BASE_FOLDER)
    with open(PATHS['custom_config_file'], 'r') as f:
        data = f.read()
    data = data.replace('repo_user: okfn', f'repo_user: {repo_user}')
    data = data.replace('repo_name: okfn-collaborative-docs', f'repo_name: {repo_name}')
    with open(PATHS['custom_config_file'], 'w') as f:
        f.write(data)

    # Move the original README.md to README-orig.md
    # Ensure to do this only one time
    readme_orig = PATHS['base_folder'] / 'README-orig.md'
    if readme_orig.exists():
        click.echo('README-orig.md already exists. Skipping new README file')
    else:
        readme = PATHS['base_folder'] / 'README.md'
        readme.rename(readme_orig)

        # Create new README.md with the link for our docs
        # TODO use jinja and a template file
        with open(readme, 'w') as f:
            f.write(f'# {repo_name}\n\n')
            f.write(f'You can see this documentation at https://{repo_user}.github.io/{repo_name}/  \n\n')
            f.write('Feel free to contribute to this project or create issues\n')
            f.write(f'at https://github.com/{repo_user}/{repo_name}/issues  \n')


if __name__ == '__main__':
    cli()
