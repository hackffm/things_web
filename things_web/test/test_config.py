import helper_test

from components import *
from resources import *
from things import *

from time import sleep

# resources
home_path = helper_test.path_home()
name = 'things'
section = 'test'
debug = True
helper_test.file_delete(home_path + '/' + name + '/' + section + '.json')
config = Config(name, section, home_path, debug)
cfg = config.cfg()
config.configuration['test'] = 'hello hello'
config.path_config = home_path + '/' + name + '/' + section + '1.json'
config.save()
_config = config.configuration['default']
print('_log_location = ' + _config['log_location'])
print('_log_file = ' + _config['log_file'])

print('pre configured nodes serial')
for ns in cfg.nodes_serial:
    print(ns['ID'])
    
print('restricted serial ports')
for rp in cfg.serial.ports.restricted:
    print(rp)
