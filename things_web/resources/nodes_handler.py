from random import random
import serial
import serial.tools.list_ports
import uuid

from things import *


class NodesHandler:
    def __init__(self, cfg, debug=False):
        self.cfg = cfg
        self.debug = debug
        
        self.nodes_not_verified = []
        if len(cfg.nodes_serial) > 0:
            for ns in cfg.nodes_serial:
                self.nodes_not_verified.append(NodeSerial(ns['ID'], self.debug))
        self.nodes_verified = []
        self.name = 'NodesHandler'
        self.serial_ports = []

    def node_exists(self, n_id):
        for nv in self.nodes_verified:
            if nv.id == n_id:
                return True

    def nodes_not_verified_remove(self, id):
        nnv = len(self.nodes_not_verified)
        for num in range(nnv):
            if self.nodes_not_verified[num].id == id:
                self.nodes_not_verified.remove(self.nodes_not_verified[num])
            else:
                num += 1
        return

    def nodes_verify(self):
        ports = []
        if self.debug:
            print('Verify serial ports')
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            for rp in self.cfg.serial.ports.restricted:
                if rp in p.description:
                    return
            if self.debug:
                print('description is  ' + p.description + ' on port ' + p.device)
            try:
                ser = serial.Serial(p.device, 38400, timeout=5)
                NS1 = NodeSerial(str(uuid.uuid4()), self.debug)
                NS1.verify(ser)
                if NS1.verified:
                    if not self.node_exists(NS1.id):
                        self.nodes_verified.append(NS1)
                        self.nodes_not_verified_remove(NS1.id)
            except serial.SerialException as e:
                if self.debug:
                    print('[' + self.name + '] error:' + str(e))

    def nodes_verified_write(self, id,  command):
        if self.debug:
            print('Write to {} command {}'.format(id, command))
        for ns in self.nodes_verified:
            if ns.id == id:
                ns.write(command)

    def thing_read(self, id):
        result = 'thing not found'
        for ns in self.nodes_verified:
            for thing in ns.things:
                if thing.id == id:
                    result = ns.NS1.read()
        return result
