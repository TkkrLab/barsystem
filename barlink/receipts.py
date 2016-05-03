import serial
import time

class ReceiptPrinter:
    ALIGN_LEFT = 0
    ALIGN_CENTER = 1
    ALIGN_RIGHT = 2

    PRINTMODE_FONT_A = 0x00
    PRINTMODE_FONT_B = 0x01
    PRINTMODE_EMPHASIZED = 0x08
    PRINTMODE_DOUBLE_HEIGHT = 0x10
    PRINTMODE_DOUBLE_WIDTH = 0x20
    PRINTMODE_UNDERLINE = 0x80


    CMD_ESC = b'\x1B'
    CMD_GS = b'\x1D'

    CODE_TABLES = {
        'cp437': b'\x00',
        'cp850': b'\x02',
        'cp858': b'\x13',
    }

    def __init__(self, device):
        self.serial = serial.Serial(
            port=device,
            baudrate=19200,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS)
        self.encoding = 'ascii'
        self.init()

    def output(self, *data):
        # print(repr(data))
        for block in data:
            self.serial.write(block)

    def init(self):
        self.output(self.CMD_ESC, b'@')

    def set_code_table(self, name):
        if name in self.CODE_TABLES:
            self.encoding = name
            self.output(self.CMD_ESC, b't', self.CODE_TABLES[name])

    def set_print_mode(self, modes):
        self.output(self.CMD_ESC, b'!', bytes([modes]))

    def set_align(self, align):
        self.output(self.CMD_ESC, b'a', bytes([align]))

    def print_image(self, filename):
        with open(filename, 'rb') as f:
            self.output(f.read())

    def writeline(self, data=None):
        if data:
            self.output(data.encode(self.encoding))
        self.output(b'\n')
        # print('>>>', data if data else '')

    def write_product_line(self, text, number):
        number_text = ' €{:.2f}'.format(number)
        number_len = len(number_text)
        text_len = 54 - number_len
        self.writeline('{text:<{text_len}}{number}'.format(text=text, number=number_text, text_len=text_len))

    def cut(self, cut_mode=0):
        self.output(self.CMD_GS, b'V', bytes([cut_mode]))

    def open_drawer(self):
        # send pulse to pin 0, 0x3c * 2ms on, 0x78 * 2ms off
        self.output(self.CMD_ESC, b'p\x00\x3C\x78')

    def feed(self, line_count=0):
        self.output(self.CMD_ESC, b'd', bytes([line_count]))
