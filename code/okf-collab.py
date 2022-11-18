from pathlib import Path

import click
import yaml


BASE_CONFIG_FILE = 'base.yml'
CUSTOM_CONFIG_FILE = 'custom.yml'
BASE_CONFIG_FOLDER = Path(__file__).resolve().parent.parent / 'conf'


@click.group()
def cli():
    pass


@cli.command()
@click.option('--dest-file', '-d', help='Destination final config file')
def build(dest_file):
    """ Build the config file """
    base_config = yaml.safe_load(open(BASE_CONFIG_FOLDER / BASE_CONFIG_FILE))
    custom_config = yaml.safe_load(open(BASE_CONFIG_FOLDER / CUSTOM_CONFIG_FILE))

    # Detect languages to prepare final custom mkdocs
    languages = custom_config['site_name'].keys()
    click.echo(f'Languages: {languages}')

    # TODO

if __name__ == '__main__':
    cli()
