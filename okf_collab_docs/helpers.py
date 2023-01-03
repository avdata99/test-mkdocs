from pathlib import Path
import os
import shutil
import yaml
from jinja2 import Template


def get_lang_setting(cfg_dict, lang, key):
    """ Get the language-specific setting from the config dict """

    if key not in cfg_dict:
        raise ValueError(f'Key "{key}" not found in config dict')
    if lang not in cfg_dict[key]:
        raise ValueError(f'Language "{lang}" not found for setting "{key}" in config')

    return cfg_dict[key][lang]


def get_list_setting(cfg_list, key):
    """ Get a dict value from a list of dicts """

    for dct in cfg_list:
        if list(dct.keys())[0] == key:
            return dct[key]


def _update_md_folder(docs_folder, context, fix_folder_fn):
    """ Update the MD files with extra values within a folder """
    if not os.path.exists(docs_folder):
        raise Exception(f'Docs folder not found: {docs_folder} at {os.getcwd()}')
    for root, dirs, files in os.walk(docs_folder):
        for file in files:
            print(f'Checking file {root} {file}')
            orig_file = os.path.join(root, file)
            dest_file = os.path.join(fix_folder_fn(root), file)
            if file.endswith(".md"):
                print(f'Fixing {orig_file} -> {dest_file}')
                with open(orig_file, "r") as f:
                    template = Template(f.read())
                with open(dest_file, "w") as f:
                    f.write(template.render(context))
            else:
                # Copy the file
                shutil.copyfile(orig_file, dest_file)

        for dir in dirs:
            _update_md_folder(os.path.join(root, dir), context, fix_folder_fn)


def update_md_files(docs_folder, config_folder, context):
    """ Update the MD files with extra values.
        Return a fixed folder path to use in the config file. """

    # Change dir to fit the config folder
    pwd = os.getcwd()
    os.chdir(config_folder)
    parts = docs_folder.split('/')
    parts[-1] = f"fixed-{parts[-1]}"
    fixed_folder = '/'.join(parts)
    print(f'Fixing MD files in {docs_folder} -> {fixed_folder}')

    if os.path.exists(fixed_folder):
        print(f'Cleaning the fixed folder {fixed_folder}')
        shutil.rmtree(fixed_folder)

    def fix_folder_fn(folder):
        dest_folder = folder.replace(docs_folder, fixed_folder)
        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)
        return dest_folder

    _update_md_folder(docs_folder, context, fix_folder_fn)

    # Back to previous folder
    os.chdir(pwd)
    return fixed_folder


def update_language_paths(config, env='local'):
    """ Each language has a base path that needs to be defined.
        This function overrides the config with the correct values. """

    alternate = config['custom_extra']['alternate']
    new_list = []
    for lang in alternate:
        lang_code = '' if lang['lang'] == 'en' else lang['lang']
        if env == 'prod':
            new_base_path = config.get('public_url_base_path', '')
            lang['link'] = f'{new_base_path}/{lang_code}'
        else:
            lang['link'] = f'/{lang_code}'
        new_list.append(lang)
    config['custom_extra']['alternate'] = new_list


def update_gh_action_language_files(gh_workflow_file_path, langs):
    """ Update the CONFIG_FILES setting from the actions file /.github/workflows/page.yml
        We need to be sure that the language files are updated and in the rigth order
        (EN must be the last one). """

    # yaml lib destroys the YAML file, manually it's better

    f = open(gh_workflow_file_path, 'r')
    lines = f.readlines()
    f.close()

    updated_lines = []
    auto_comment = '# Automatically updated, commit and do not change'
    for line in lines:
        if line.strip().startswith(auto_comment):
            continue
        if line.strip().startswith('CONFIG_FILES'):
            all_but_en = [lang for lang in langs if lang != 'en']
            config_files = " ".join([f"conf/mkdocs-{lang}.yml" for lang in all_but_en])
            line = f'          CONFIG_FILES: {config_files} conf/mkdocs-en.yml\n'
            updated_lines.append(f'          {auto_comment}\n')
        updated_lines.append(line)

    f = open(gh_workflow_file_path, 'w')
    f.writelines(updated_lines)
    f.close()


def get_yaml(yaml_path):
    if not os.path.exists(yaml_path):
        raise Exception(f'YAML file does not exists {yaml_path}')
    try:
        yaml_data = yaml.safe_load(open(yaml_path))
    except yaml.parser.ParserError as e:
        raise Exception(f'YAML file is not valid YAML {yaml_path}') from e
    return yaml_data


def get_paths(base_folder):
    base_path = Path(base_folder)
    base_config_folder = base_path / 'conf'
    base_page_folder = base_path / 'page'
    site_folder = base_path / 'site'
    ret = {
        'base_folder': base_path,
        'base_config_folder': base_config_folder,
        'base_page_folder': base_page_folder,
        'base_config_file': base_config_folder / 'base.yml',
        'custom_config_file': base_config_folder / 'custom.yml',
        'site_folder': site_folder,
        'user_assets_folder': base_page_folder / 'assets',
        'site_assets_folder': site_folder / 'assets',
    }

    return ret


def validate_nav_lang_exists(nav, lang):
    if f'nav-{lang}' not in nav:
        raise Exception(f'No "nav-{lang}" sub-section found in the "nav" section from your custom config file')


def validate_index_lang_file(nav, lang):
    for page in nav:
        if 'index.md' in page.values():
            break
    else:
        raise Exception(f'No "index.md" found in the "nav-{lang}" sub-section from your custom config file')


def add_pdf_url(config, wpdf_plugin, language):
    """ Add a final PDF URL for this language config"""
    base_url = config['site_url'].rstrip('/')
    rel_pdf_url = wpdf_plugin['output_path'].lstrip('/')
    if language == 'en':
        config['extra']['pdf_url'] = f'{base_url}/{rel_pdf_url}'
    else:
        config['extra']['pdf_url'] = f'{base_url}/{language}/{rel_pdf_url}'
    config['nav'].append(
        {'PDF': config['extra']['pdf_url']}
    )


def validate_langs(custom_config):
    """ Validate that the languages in site_name and alternate are the same """

    languages = list(custom_config['site_name'].keys())
    langs_in_alternate = [
        alt['lang']
        for alt in custom_config['custom_extra']['alternate']
    ]
    if languages != langs_in_alternate:
        raise Exception(
            f'Languages in site_name and alternate do not match: {languages} != {langs_in_alternate}'
        )
    return languages
