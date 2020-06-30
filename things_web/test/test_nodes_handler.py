import helper_test

from time import sleep

from resources import *

home_path = helper_test.path_home()
name = 'things'
section = 'test'
debug = True
helper_test.file_delete(home_path + '/' + name + '/' + section + '.json')
config = Config(name, section, home_path, debug)
cfg = config.cfg()

nh = NodesHandler(cfg, debug)
nh.debug = debug
nh.nodes_verify()
len_not_verified = len(nh.nodes_not_verified)
print('Number of not verified Nodes is ' + str(len_not_verified))
if len_not_verified > 0:
    print('not verified nodes')
    for num in range(len_not_verified):
        print(nh.nodes_not_verified[num].id)

len_verified = len(nh.nodes_verified)
node_test = 'Node1'
thing_test = 'door1'
command_open = 'o'
command_close = 'c'
print('\nNumber of verified Nodes is ' + str(len_verified))
if len_verified > 0:
    print('verified nodes')
    for node in nh.nodes_verified:
        print(node.id)
    print('write directly to ' + node_test)
    for node in nh.nodes_verified:
        if node.id == node_test:
            node.write(thing_test + ':' + command_open)
            sleep(1.5)
            node.write(thing_test + ':' + command_close)
    sleep(2.0)

    print('\nread whats left')
    for node in nh.nodes_verified:
        print('node ' + str(node.id) + ' has')
        print(node.read_string())
