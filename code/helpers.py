import os
import shutil
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
    """ Update the MD files with extra values within a fodler """
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

    def fix_folder_fn(folder):
        dest_folder = folder.replace(docs_folder, fixed_folder)
        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)
        return dest_folder

    _update_md_folder(docs_folder, context, fix_folder_fn)

    # Back to previous folder
    os.chdir(pwd)
    return fixed_folder
