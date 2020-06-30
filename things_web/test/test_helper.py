import helper_test

from components import *
from resources import *
from things import *

from time import sleep

# resources
home_path = helper_test.path_home()
name = 'thing'
section = 'test'
debug = True
helper_test.file_delete(home_path + '/' + name + '/' + section + '.json')
config = Config(name, section, home_path, debug)
cfg = config.cfg()
config.configuration['test'] = 'hello hello'
config.path_config = home_path + '/' + name + '/' + section + '1.json'
config.save()
config.load()
configuration = config.configuration
cfg = config.cfg()
debug = cfg.debug
helper = Helper(configuration)
