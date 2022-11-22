from pathlib import Path
import click
import yaml
from helpers import get_lang_setting, get_list_setting


BASE_CONFIG_FILE = 'base.yml'
CUSTOM_CONFIG_FILE = 'custom.yml'
BASE_CONFIG_FOLDER = Path(__file__).resolve().parent.parent / 'conf'


@click.group()
def cli():
    pass


@cli.command()
def build():
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

        # TODO
        # extra - alternate
        # extra assets_folder -> use github URL?
        # Allow custom PDF settings (cover_title, cover_subtitle, etc)
        # run `okf-collab build` in gh-action

        # write the final config file
        final_config_file = BASE_CONFIG_FOLDER / f'mkdocs-{language}.yml'
        with open(final_config_file, 'w') as f:
            yaml.dump(config, f)
        click.echo(f'Config file written to {final_config_file}')


if __name__ == '__main__':
    cli()
