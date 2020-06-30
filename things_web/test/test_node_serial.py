import helper_test

import serial.tools.list_ports
from time import sleep

from things import *

debug = True
ports = []
ser = None

NS1 = NodeSerial('NS1', debug)
print('Verify serial ports')
ports = list(serial.tools.list_ports.comports())
if len(ports) == 0:
    print('no used ports found')
for p in ports:
    print('description is ' + p.description + ' on port ' + p.device)
    ser = serial.Serial(p.device, 38400, timeout=5)
    NS1.verify(ser)

print('NS1 verification is ' + str(NS1.verified))
print('NS1 id is ' + NS1.id)

ports = []
print('do it again as some may hang during warm up phase')
NS2 = NodeSerial('NS2', debug)
print('\nVerify serial ports')
ports = list(serial.tools.list_ports.comports())
if len(ports) == 0:
    print('no used ports found')
for p in ports:
    print('description is ' + p.description + ' on port ' + p.device)
    ser = serial.Serial(p.device, 38400, timeout=5)
    NS2.verify(ser)

print('\nNS 2 verification is ' + str(NS2.verified))

if NS2.verified:
    print(NS2.id + ' has these things')
    for thing in NS2.things:
        print(thing.id)

    print('use the usual things')
    for thing in NS2.things:
        _id = str(thing.id)
        if 'door1' in _id.lower():
            print('N2 is verified start working with door1')
            command_open = 'door1:O'
            command_close = 'door1:C'
            NS2.write(command_open)
            sleep(2.0)
            result = NS2.read_string()
            print('result of command_open is ' + result)
            NS2.write(command_close)
            sleep(2.0)
            result = NS2.read_string()
            print('result of command_close is ' + result)
        if 'btm01' in _id.lower():
            print('\nget state of btm01')
            thing_name = 'btm01'
            result = NS2.thing_state(thing_name)
            print('result is ' + result)
        if 'led13' in _id.lower():
            NS2.write('led13')
            sleep(2.0)
            result = NS2.read_string()
            print('result of command led13 is ' + str(result))
            sleep(2.0)
            result = NS2.read_string()
            print('now led13 is ' + str(result))
