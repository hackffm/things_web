import json
import os


class Struct(object):
    def __init__(self, adict):
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)

    def items(self):
        return self.__dict__.items()

    def __iter__(self):
        return self.__dict__.__iter__()


class Config:

    def __init__(self, name=False, section=False, path_home='', debug=False):

        if not name:
            name = 'serial_things'
        if not section:
            section = name

        self.configuration = ''
        self.debug = debug
        self.name = name
        self.section = section

        self.path_config = path_home + '/' + self.name + '/' + self.section + '.json'
        self.path_home = path_home
        self.load()

    def cfg(self):
        return Struct(self.configuration)

    def default(self):
        # booleans must be no strings here !
        _config = {
            self.name: {
                'port': 9000
            },
            'nodes_serial': [
                {
                    'ID': 'MU'
                },
                {
                    'ID': 'A2'
                },
                {
                    'ID': 'Node1'
                },
            ],
            'debug': True,
            'default': {
                "log_file": self.section + ".log",
                "log_location": self.path_home + "/" + self.name +"/log",
            },
            'serial' : {
                'ports' : {
                    'restricted' : ['ttyAMA0']
                }
            }
        }
        return _config

    def load(self):
        if os.path.exists(self.path_config):
            if self.debug:
                print('load config from', self.path_config)
            with open(self.path_config) as json_data:
                self.configuration = json.load(json_data)
        else:
            if self.debug:
                print('new config', self.path_config)
            self.configuration = self.default()
            self.save()
        return

    def save(self):
        data = json.dumps(self.configuration, indent=4)
        _dir = os.path.dirname(self.path_config)
        if not os.path.exists(_dir):
            if self.debug:
                print('create folder ', _dir)
            os.makedirs(_dir)
        with open(self.path_config, 'w') as outfile:
            outfile.write(data)
        if self.debug:
            print('new config saved in', self.path_config)
        return True
