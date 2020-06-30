import datetime
import os
import netifaces
import socket
import subprocess

from os import listdir
from os.path import isfile, join
from time import sleep


class Helper:

    def __init__(self, configuration):
        self.configuration = configuration
        self.default = self.configuration['default']

    def infos(self):
        infos = []
        infos.append('hostname ' + str(socket.gethostname()))
        infos.append('PID ' + str(os.getpid()))
        ifaces = self.interfaces_self()
        for iface in ifaces:
            infos.append('Interface' + str(iface))
        return infos

    def interfaces_first(self):
        ips = self.interfaces_self()
        # remove ipv6 from results
        for ip in ips:
            if ':' not in ip:
                return ip
        return '127.0.0.1'

    def interfaces_self(self):
        ifaces = []
        for interface in netifaces.interfaces():
            if interface != 'lo':
                if 2 in netifaces.ifaddresses(interface):
                    _i = netifaces.ifaddresses(interface)
                    _i = _i[2][0]['addr']
                    if self.not_local(_i):
                        ifaces.append(_i)
                if 17 in netifaces.ifaddresses(interface):
                    _i = netifaces.ifaddresses(interface)
                    _i = _i[17][0]['addr']
                    if self.not_local(_i):
                        ifaces.append(_i)
                if 18 in netifaces.ifaddresses(interface):
                    _i = netifaces.ifaddresses(interface)
                    _i = _i[18][0]['addr']
                    if self.not_local(_i):
                        ifaces.append(_i)
        return ifaces

    def file_delete(self, file_path):
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            return 'done'
        else:
            return 'not found'

    def files_in_path(self, file_path):
        files = [f for f in listdir(file_path) if isfile(join(file_path, f))]
        return files

    def folder_create_once(self, folder_path):
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            return True
        except IOError as e:
            print('Error[Helper]' + str(e))
            return False

    def log_add_text(self, name, text):
        l_home, pre_text = self.log_home(name)
        text = self.now_str() + ': ' + pre_text + ' ' + str(text)
        with open(l_home, 'a') as outfile:
            outfile.write(text + '\n')

    def log_home(self, name):
        _config = self.default
        _log_location = _config['log_location']
        _log_file = _config['log_file']
        _pre_text = name + ':'
        if name in self.configuration:
            _config = self.configuration[name]
            if 'log_location' in _config:
                _log_location = _config['log_location']
            if 'log_file' in _config:
                _log_file = _config['log_file']
                _pre_text = ''
        log_home_path = _log_location + '/' + _log_file
        self.folder_create_once(_log_location)
        return [log_home_path, _pre_text]

    def not_local(self, ip):
        if ip != '127.0.0.1':
            return True
        return False

    def now_str(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def shutdown(self, time):
        _down = int(time)
        print('fpvcar down in ' + str(_down))
        sleep(_down)
        print('os shudown in 10')
        try:
            subprocess.call(['sleep 10s;sudo shutdown -h now'], shell=True)
            return 'os going down'
        except Exception as e:
            return str(e)
