import json
import os
import sys

import tornado.httpserver
import tornado.web
import tornado.websocket

from multiprocessing import Process
from time import sleep
from tornado import gen
from tornado.ioloop import IOLoop

from resources import *
from web_handlers import *


def path_home():
    _path = os.getenv('USERPROFILE')
    if _path == '' or _path == None:
        _path = os.getenv('HOME')
    _path = str(_path)
    _path = _path.replace('\\', '/')
    return _path


# resources
name = 'things'
section = 'things_web'
debug = True
config = Config(name, section, path_home(), debug)
config.load()
configuration = config.configuration
cfg = config.cfg()
debug = cfg.debug
helper = Helper(configuration)

nodes_handler = NodesHandler(cfg, debug)
#nodes_handler.nodes_verify()


def websocket_write(message):
    if debug:
        print('websocket_write:' +str(message))
    if type(message) == dict:
        message = json.dumps(message)
        [con.write_message(message) for con in WebSocketHandler.connections]
    else:
        [con.write_message(message) for con in WebSocketHandler.connections]


async def websocket_write_loop():
    while True:
        for node in nodes_handler.nodes_verified:
            node_text = node.read_string()
            if len(node_text) > 0:
                websocket_write(node_text)
        await gen.sleep(0.3)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def initialize(self, debug=False):
        self.debug = debug
        self.name = 'WebSocketHandler'

    def log(self, text):
        print(self.name + ' ' + text)

    def valid_jasonparse(self, text):
        text = text.replace('\'', '\\"')
        text = text.replace('True', 'true')
        text = text.replace('False', 'false')
        return text

    # websocket abstract methods
    def check_origin(self, origin):
        return True

    def open(self):
        self.connections.add(self)
        if self.debug:
            self.log('new connection was opened')
        pass

    def on_close(self):
        self.connections.remove(self)
        if self.debug:
            self.log('connection closed')
        pass

    def on_message(self, message):
        try:
            m = message
            if m.startswith('{'):
                m = json.loads(message)
            else:
                message = message.split(':')
                m = {'node': message[0], 'thing': {'id': message[1], 'command': message[2]}}
            self.log('on_message:' + str(m))
            if 'node' in m:
                _node = m['node']
                _command = ''
                if 'thing' in m:
                    _thing = m['thing']['id']
                    _command = m['thing']['command']
                    if len(_command) > 0:
                        _command = _thing + ':' + _command
                    else:
                        _command = _thing
                if 'command' in m:
                    _command = m['command']
                # print('[debug][things_web]write node ' + _node + ' command ' + _command)
                nodes_handler.nodes_verified_write(_node, _command)
                return
            else:
                # should be never here
                self.log('on_message:can not handle' + str(m))
        except Exception as e:
            self.log('on_message failed with ' + str(e))
        return


class WebApplication(tornado.web.Application):
    def __init__(self, port, debug=False):
        current_path = os.path.dirname(os.path.abspath(__file__))
        web_resources = current_path + '/web_resources'

        handlers = [
            (r'/', HandlerIndexPage, dict(helper=helper)),
            (r'/things', HandlerThingsPage, dict(helper=helper,  port=port, nodes_handler=nodes_handler)),
            (r'/websocket', WebSocketHandler, dict(debug=debug))
        ]

        settings = {
            'autoreload': debug,
            'debug': debug,
            'static_path': web_resources,
            'template_path': 'web_templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class WebServer:
    def __init__(self, helper, debug=False):
        address = self.address()
        port = configuration[name]['port']
        ws_app = WebApplication(port, debug)
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(port, address=address)

        print('Start things_web http://' + address + ':' + str(port))
        helper.log_add_text('things_web', 'Start things_web at address ' + address + ' port:' + str(port))
        IOLoop.current().spawn_callback(websocket_write_loop)
        IOLoop.instance().start()

    def address(self):
        _address = helper.interfaces_first()
        if 'address' in configuration[name]:
            _address = configuration[name]['address']
        return _address


if __name__ == '__main__':
    running = True
    try:
        # start processes
        print('start things web server')
        p1 = Process(target=WebServer(helper, debug))
        p1.daemon = True
        p1.start()
        print('PID Webserver', p1.pid)
        while running:
            sleep(0.5)

    except KeyboardInterrupt:
        print('ending with keyboard interrupt')
        running = False
        p1.terminate()
    except Exception as e:
        print('[things_web]error in __main__ ' + str(e))

    running = False
    print('[things_web]bye')
    sys.exit()
