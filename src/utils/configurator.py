import os
from configparser import ConfigParser

# module names
LOAD_GHSEARCH = 'load_ghsearch'
EXTRACTOR = 'repo_extractor'

# entry names
GHSEARCH = 'ghsearch'
IMPORTFILE = 'importfile'
EXTENSIONS = 'language'
KEYWORDS = 'keywords'
POSTGRESQL = 'postgresql'
RUN_PARALLEL = 'run_parallel'
GITHUB = 'github'
PERSONAL_ACCESS_TOKEN = 'personal_access_token'
LIST_FILES = 'list_files'

# INI_FILE contains the default location of the configuration
INI_FILE = \
    os.path.realpath(os.path.join(os.path.dirname(__file__),
                                  '../..', 'var', 'commitextractor.ini'))

inifile = INI_FILE

INI_FILE2 = \
    os.path.realpath(os.path.join(os.path.dirname(__file__),
                                  '../..', 'var', 'analysis.ini'))

inifile2 = INI_FILE2


# get_number_of_processes returns the number of processes for which the application is configured
def get_number_of_processes(module_name: str) -> int:
    return int(get_module_configurationitem(module_name, RUN_PARALLEL))


# get_database_configuration returns a list of database connection parameters
def get_database_configuration():
    config = ConfigParser()
    config.read(inifile)

    db = {}
    if config.has_section(POSTGRESQL):
        params = config.items(POSTGRESQL)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(POSTGRESQL, inifile))

    return db


def get_extensions():
    return get_module_configurationitem(EXTRACTOR, 'list_extensions').replace(' ', '').split(',')


def get_keywords():
    return get_module_configurationitem(KEYWORDS, 'list_keywords').replace(' ', '').split(',')


def get_keywords_lib():
    return get_module_configurationitem(KEYWORDS, 'list_keywords_lib').replace(' ', '').split(',')


def get_files():
    config = ConfigParser()
    config.read(inifile)

    # get section
    if config.has_option(EXTRACTOR, LIST_FILES):
        return get_module_configurationitem(EXTRACTOR, LIST_FILES).replace(' ', '').split(',')
    else:
        return []


def get_main_language():
    return get_module_configurationitem('language', 'main_language').replace(' ', '').split(',')


# get_ghsearch_importfile returns the file from which a list of projects can be added to be extracted.
def get_ghsearch_importfile():
    return get_module_configurationitem(module=LOAD_GHSEARCH, entry='importfile')


def get_github_personal_access_token():
    return get_module_configurationitem(GITHUB, PERSONAL_ACCESS_TOKEN)


# set_inifile makes the ini_file dynamic.
# this function is used for test purposes only.
def set_inifile(newfile=INI_FILE):
    global inifile
    inifile = newfile


def get_module_configurationitem(module: str, entry: str) -> str:
    config = ConfigParser()
    config.read(inifile)

    # get section
    if config.has_option(module, entry):
        value = config[module][entry]
    else:
        raise Exception('Option {0} not found in the {1} module'.format(entry, module))

    return value


def get_module_configurationitem_boolean(module: str, entry: str) -> bool:
    """
    Returns a boolean value for an item
    Default value False if item is lacking in ini file
    Value for the entry should be either 0 (False) or 1 (True)
    :param module:
    :param entry:
    :return:
    """
    config = ConfigParser()
    config.read(inifile)
    value = False

    if config.has_option(module, entry):
        value = bool(int(config[module][entry]))

    return value
