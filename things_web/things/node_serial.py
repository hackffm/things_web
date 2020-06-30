import serial
from time import sleep

from .thing import Thing


class NodeSerial(Thing):

    def __init__(self, id, debug=False):
        super().__init__(id, debug)
        self.message = ''
        self.things = []           # list of { 'ID', VALUE}
        self.ser = None
        self.result = ''
        self.verified = False

    def handleMessage(self, message):
        if self.debug:
            print(self.name + ' received ' + str(message))
        self.message = message

    def clean_buffer(self):
        result = 'not Empty'
        sleep(1.0)
        while len(result) > 0:
            result = self.read_string()
            if self.debug:
                print('buffer is ' + result)

    def thing_add(self, thing):
        if not self.thing_exists(thing.id):
            self.things.append(thing)
            return 'added'
        else:
            return 'thing already exists'

    def thing_exists(self, id):
        for ty in self.things:
            if ty.id == id:
                return True
        return False

    def thing_state(self, thing_name):
        self.clean_buffer()
        result = 'None'
        if self.thing_exists(thing_name):
            self.write(thing_name)
            sleep(3.0)
            result = self.read_string()
        return result

    def verify(self, ser):
        if not ser:
            # we return here only for testing
            return
        sleep(2.0)
        self.ser = ser
        self.write('?')
        sleep(2.0)
        rs = self.read_string()
        verified = self.verify_node_string(rs)
        if verified:
            self.verified = True
            if self.debug:
                print(self.ser.portstr + ' verified as ' + rs)
        else:
            self.ser = None
            self.verified = False
            if self.debug:
                print('Not verified')
        return

    def verify_node_string(self, node_string):
        things = []
        if len(node_string) < 2:
            return False
        if ':' not in node_string:
            return False
        # varified from here
        _string = node_string.split(':')
        _node = _string[0]
        things = _string[1]
        if ',' in things:
            things = things.split(',')
            for thing in things:
                self.things.append(Thing(thing))
        else:
            self.things.append(Thing(things))
        self.id = _node
        return True

    def read(self):
        data = b''
        wait_bytes = self.ser.inWaiting()
        # loud debug print(str(wait_bytes) + ' bytes waiting in serial port')
        for i in range(wait_bytes):
            b = self.ser.read(1)
            if b != b'\r':
                if b == b'\n':
                    return data
                else:
                    data += b
        return data

    def read_string(self):
        result = self.read()
        if isinstance(result, bool):
            result = str(result)
        else:
            result = str(result.decode())
        return result

    def write(self, command):
        if self.debug:
            print('[debug][node_serial]id:' + str(self.id) + ' ser.write ' + str(command))
        command = str(command) + '\r'
        try:
            self.ser.write(command.encode())
        except Exception as e:
            if self.debug:
                print(e)
        return
