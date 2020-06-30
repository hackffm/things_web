import serial
import serial.tools.list_ports
from time import sleep


def verify():
    print('Verify serial ports')
    ports = list(serial.tools.list_ports.comports())
    if len(ports) == 0:
        print('no used ports found')
    for p in ports:
        print('use serial Port ' + p.device)
        ser = serial.Serial(p.device, 38400, timeout=5)
        print('write ?\\r to ' + p.description + ' on port ' + p.device)
        sleep(2.0)
        write(ser, '?')
        sleep(2.0)
        sr = read_string(ser)
        if len(sr) >= 2:
            print(ser.portstr + ' did answer ' + str(sr))
        else:
            print(ser.portstr + ' did not answer')


def read(ser):
    data = b''
    wait_bytes = ser.inWaiting()
    print(str(wait_bytes) + ' bytes waiting in serial port')
    for i in range(wait_bytes):
        b = ser.read(1)
        if b != b'\r':
            if b == b'\n':
                return data
            else:
                data += b
    return data


def read_string(ser):
    result = read(ser)
    if isinstance(result, bool):
        result = str(result)
    else:
        result = str(result.decode())
    return result


def write(ser, command):
    print('ser.write ' + str(command))
    command = str(command) + '\r'
    try:
        ser.write(command.encode())
    except Exception as e:
        print(e)
    return


verify()
