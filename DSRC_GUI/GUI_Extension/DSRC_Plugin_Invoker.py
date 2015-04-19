__author__ = 'xuepeng'

import ConfigParser
import sys
import os


class Plugin:
    def __init__(self, executor_m=None):
        self.executor_module = executor_m

plugins = {}

plugin_name = None

executor_module = None


def get_executor_module():
    global executor_module
    return executor_module


def set_plugin(name):
    global executor_module
    global plugin_name
    global plugins
    plugin = plugins[name]
    if plugin:
        executor_module = plugin.executor_module
        plugin_name = name


def load_plugin():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser.SafeConfigParser()
    config_ini_path = ''.join([dir_path, "/config.ini"])
    print config_ini_path
    config.read(config_ini_path)
    try:
        plugins_config = dict(config.items('Plugins'))
        for key in plugins_config:
            value = plugins_config[key]
            load_a_plugin(key, value)
    except Exception, e:
        print e

    try:
        default_name = config.get('Default', 'default')
        set_plugin(default_name)
    except Exception, e:
        print e

    print "All plugins loaded"


def load_a_plugin(name, config_file):
    global plugins
    a_executor_module = None
    # Initialize plugins
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser.SafeConfigParser()
    config_ini_path = ''.join([dir_path, "/", config_file])
    print config_ini_path

    config.read(config_ini_path)

    plugin = Plugin()

    try:
        path_executor = config.get('CustomizedExecutor', 'DirectoryPath')
        file_executor = config.get('CustomizedExecutor', 'FileName')
        executor_module_name = config.get('CustomizedExecutor', 'ModuleName')
        if path_executor:
            if path_executor == "./":
                if dir_path not in sys.path:
                    sys.path.append(''.join([dir_path, '/']))
            else:
                if os.path.exists(path_executor + file_executor):
                    if path_executor not in sys.path:
                        sys.path.append(path_executor)
                else:
                    raise Exception("Executor Plugin path error!")
        if executor_module_name:
            a_executor_module = __import__(executor_module_name)
            plugin.executor_module = a_executor_module
    except Exception, e:
        print e

    if a_executor_module:
        print executor_module_name

    plugins[name] = plugin


def customized_execute(console):
    global executor_module
    if executor_module:
        executor_module.execute(console)