# command interpreter for CircuitPython 4.x
import board
import pulseio
import supervisor
import sys

from time import sleep
from adafruit_motor import servo
from digitalio import DigitalInOut, Direction, Pull

led13 = DigitalInOut(board.D13)
led13.direction = Direction.OUTPUT

# create a PWMOut object on M4 Pin A1.
pwm = pulseio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)
# For Gemma M0, Trinket M0, Metro M0 Express, ItsyBitsy M0 Express, Itsy M4 Express
switch = DigitalInOut(board.D2)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)

angle_open = 10
angle_closed = 150
btm_pushed = 'pushed'
btm_pushed_not = 'not pushed'
state_btm01 = btm_pushed_not
led13.value = False
node_name = 'Node1'


def cmd_id():
    text = node_name + ':'
    for cd in cmd_dict:
        text = text + cd + ','
    text = text[:-1]
    print(text)
    return


def cmd_btm01(arg):
    global state_btm01
    global node_name
    print(node_name + ':btm01:' + state_btm01)
    state_btm01 = btm_pushed_not
    return


def cmd_door1(arg):
    arg = arg.lower()
    unknown = True
    if arg == ':o':
        my_servo.angle = angle_open
        print(node_name + ":door1:o")
        unknown = False
    if arg == ':c':
        my_servo.angle = angle_closed
        print(node_name + ":door1:c")
        unknown = False
    if unknown:
        print(node_name + ":door1:unknown command=>" + arg)
    return


def cmd_led13(arg):
    if led13.value:
        led13.value = False
    else:
        led13.value = True
    sleep(0.01)
    print(node_name + ":led13:" + str(led13.value))


def switch_check(arg):
    global state_btm01
    if switch.value:
        led13.value = False
        sleep(0.01)  # debounce delay
    else:
        state_btm01 = btm_pushed
        led13.value = True
        sleep(0.01)  # debounce delay
    return


cmd_line = ""
# all commands must be 5 letters long !!
cmd_dict = {
  'door1': cmd_door1,
  'led13': cmd_led13,
  'btm01': cmd_btm01
}


def receive_serial_cmd():
    global cmd_line
    if supervisor.runtime.serial_bytes_available:
        value = sys.stdin.read(1)
        ch = ord(value)
        if 32 <= ch <= 126:           # printable character
            cmd_line += chr(ch)
        elif ch in {10, 13}:          # EOL - try to process
            if len(cmd_line) == 1:
                if cmd_line[0] == '?':
                    cmd_id()
                    cmd_line = ''
                    return
            if len(cmd_line) >= 5:
                _cmd = ''
                _arg = ''
                _cmd = cmd_line[:5]
                if _cmd in cmd_dict:
                    if len(cmd_line) >= 6:
                        _arg = cmd_line[5:]
                    cmd_dict[_cmd](_arg)
                    cmd_line = ''
                    return
                else:
                    print(node_name + ":unkown command=>" + str(cmd_line))
                    cmd_line = ''
                    return


if __name__ == '__main__':
    my_servo.angle = angle_open
    count = 0
    while True:
        count += 1
        if count >= 1000:
            print(node_name + ':alive')
            count = 0
        receive_serial_cmd()
        switch_check(switch.value)
        sleep(0.1)
