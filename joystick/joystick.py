# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

import os, struct, array
from fcntl import ioctl
import time

class Joystick(object):

    def __init__(self, dev='/dev/input/js0'):

        self.axis_states = {}
        self.button_states = {}

        # These constants were borrowed from linux/input.h
        self.axis_names = {
            0x00 : 'x',
            0x01 : 'y',
            0x02 : 'z',
            0x03 : 'rx',
            0x04 : 'ry',
            0x05 : 'rz',
            0x06 : 'trottle',
            0x07 : 'rudder',
            0x08 : 'wheel',
            0x09 : 'gas',
            0x0a : 'brake',
            0x10 : 'hat0x',
            0x11 : 'hat0y',
            0x12 : 'hat1x',
            0x13 : 'hat1y',
            0x14 : 'hat2x',
            0x15 : 'hat2y',
            0x16 : 'hat3x',
            0x17 : 'hat3y',
            0x18 : 'pressure',
            0x19 : 'distance',
            0x1a : 'tilt_x',
            0x1b : 'tilt_y',
            0x1c : 'tool_width',
            0x20 : 'volume',
            0x28 : 'misc',
        }

        self.button_names = {
            0x120 : 'trigger',
            0x121 : 'thumb',
            0x122 : 'thumb2',
            0x123 : 'top',
            0x124 : 'top2',
            0x125 : 'pinkie',
            0x126 : 'base',
            0x127 : 'base2',
            0x128 : 'base3',
            0x129 : 'base4',
            0x12a : 'base5',
            0x12b : 'base6',
            0x12f : 'dead',
            0x130 : 'a',
            0x131 : 'b',
            0x132 : 'c',
            0x133 : 'x',
            0x134 : 'y',
            0x135 : 'z',
            0x136 : 'tl',
            0x137 : 'tr',
            0x138 : 'tl2',
            0x139 : 'tr2',
            0x13a : 'select',
            0x13b : 'start',
            0x13c : 'mode',
            0x13d : 'thumbl',
            0x13e : 'thumbr',

            0x220 : 'dpad_up',
            0x221 : 'dpad_down',
            0x222 : 'dpad_left',
            0x223 : 'dpad_right',

            # XBox 360 controller uses these codes.
            0x2c0 : 'dpad_left',
            0x2c1 : 'dpad_right',
            0x2c2 : 'dpad_up',
            0x2c3 : 'dpad_down',
        }

        self.num_axes = 0
        self.num_buttons = 0

        self.axis_map = []
        self.button_map = []

        self.dev = dev
        self.jsdev = None

    def init(self):
        # Check path to device
        if not os.path.exists(self.dev):
            print(self.dev, " is missing")
            return

        # Open the joystick device.
        print('Opening %s...' % self.dev)
        # self.jsdev = jsdev = open(self.dev, 'rb')
        self.jsdev = jsdev = os.open(self.dev, os.O_RDONLY | os.O_NONBLOCK)

        # Get the device name.
        buf = array.array('B', [0] * 64)
        ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
        self.js_name = buf.tobytes().rstrip(b'\x00').decode('utf-8')
        print('Device name: %s' % self.js_name)

        # Get number of axes and buttons.
        buf = array.array('B', [0])
        ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
        self.num_axes = buf[0]

        buf = array.array('B', [0])
        ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
        self.num_buttons = buf[0]

        # Get the axis map.
        buf = array.array('B', [0] * 0x40)
        ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

        for axis in buf[:self.num_axes]:
            axis_name = self.axis_names.get(axis, 'unknown(0x%02x)' % axis)
            self.axis_map.append(axis_name)
            self.axis_states[axis_name] = 0.0

        # Get the button map.
        buf = array.array('H', [0] * 200)
        ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

        for btn in buf[:self.num_buttons]:
            btn_name = self.button_names.get(btn, 'unknown(0x%03x)' % btn)
            self.button_map.append(btn_name)
            self.button_states[btn_name] = 0

    def show_map(self):
        '''
        List the buttons and axes found on this joystick
        '''
        print('%d axes found: %s' % (self.num_axes, ', '.join(self.axis_map)))
        print('%d buttons found: %s' % (self.num_buttons, ', '.join(self.button_map)))

    def event(self):
        '''
        get the next recorded event from the joystick, record the new state
        locally and then return the event. Returns None if no events.
        Just read one event per call, that way if there is delay in the
        system, toggle events won't get missed.
        '''
        # evbuf = self.jsdev.read(8)
        try:
            evbuf = os.read(self.jsdev, 8)
        except:
            return (None, None)

        jtime, value, type, number = struct.unpack('IhBB', evbuf)

        # if type & 0x80:
        #     print("(initial)", end="")

        if type & 0x01:
            button = self.button_map[number]
            if button:
                self.button_states[button] = value
                # if value:
                #     print("%s pressed" % (button))
                # else:
                #     print("%s released" % (button))
                return (button, value)

        if type & 0x02:
            axis = self.axis_map[number]
            if axis:
                fvalue = value / 32767.0
                self.axis_states[axis] = fvalue
                # print("%s: %.3f" % (axis, fvalue))
                return (axis, fvalue)

    def get_button(self, button):
        return self.button_states.get(button, None)

    def get_axis(self, axis):
        return self.axis_states.get(axis, None)

class F710Joystick(Joystick):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.axis_names = {
            0x00: 'left_stick_horz',
            0x01: 'left_stick_vert',
            0x03: 'right_stick_horz',
            0x04: 'right_stick_vert',

            0x02: 'L2_pressure',
            0x05: 'R2_pressure',

            0x10: 'dpad_leftright', # 1 is right, -1 is left
            0x11: 'dpad_up_down', # 1 is down, -1 is up
        }

        self.button_names = {
            0x13a: 'back',
            0x13b: 'start',
            0x13c: 'Logitech',

            0x130: 'A',
            0x131: 'B',
            0x133: 'X',
            0x134: 'Y',

            0x136: 'L1',
            0x137: 'R1',

            0x13d: 'left_stick_press',
            0x13e: 'right_stick_press',
        }

        self.init()

# Main event loop
if __name__ == '__main__':
    js = F710Joystick()
    # js.show_map()

    print(js.get_button('R1'))
    while True:
        event, value = js.event()
        if event == 'R1':
            print('R1', value)
        time.sleep(.1)
        if js.get_button('R1'):
            print("R1 pressed")
