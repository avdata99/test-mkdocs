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
