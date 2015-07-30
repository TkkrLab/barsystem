import base64
import hashlib
import re
import select
import socket
import ssl
import struct
import sys
import threading
import time
import logging

from django.utils.datastructures import MultiValueDict

def readlines(sock, recv_buffer=4096, delim='\n'):
    buffer = ''
    data = True
    while data:
        data = sock.recv(recv_buffer).decode('utf-8')
        buffer += data

        while buffer.find(delim) != -1:
            line, buffer = buffer.split(delim, 1)
            yield line
    return

class SocketClosedException(Exception):
    pass

def header_split(line):
    return map(lambda x: x.strip(), line.split(':', 1))

class WebSocketConnection:
    WEBSOCK_GUID = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    OPCODE_CONTINUATION = 0x00
    OPCODE_TEXT         = 0x01
    OPCODE_BINARY       = 0x02
    OPCODE_CLOSE        = 0x08
    OPCODE_PING         = 0x09
    OPCODE_PONG         = 0x0A
    opcode_map = {
        0x00: 'continuation',
        0x01: 'text',
        0x02: 'binary',
        0x08: 'close',
        0x09: 'ping',
        0x0A: 'pong',
    }

    def __init__(self, socket, remote_addr):
        self.error = False
        self.socket = socket
        self.remote_addr, self.remote_port = remote_addr

    @property
    def addr(self):
        return self.remote_addr, self.remote_port
    
    def upgrade(self):
        result = self.handshake()
        if result == True:
            return True
        else:
            if result == False:
                self.handshakeReject()
            return False


    def handshake(self):
        reply = ''
        request_path = ''
        headers = MultiValueDict()
        for line in readlines(self.socket, delim='\r\n'):
            # print('RECV: {}'.format(line))
            if len(line) == 0:
                break
            if request_path == '':
                m = re.match('^GET (.+) HTTP/1.1', line)
                if m:
                    request_path = m.groups(1)[0]
                else:
                    self.write('HTTP/1.1 405 Method not allowed\r\n\r\n')
                    return 405
                continue
            if not ':' in line:
                continue
            key, value = header_split(line)
            headers.appendlist(key, value)
            # print(key, value)
            # if line.startswith('Sec-WebSocket'):
            #     print(line)
            # if key == 'Sec-WebSocket-Key':
        
        if headers.get('Sec-WebSocket-Version', None) != '13':
            return False
        key = headers.get('Sec-WebSocket-Key', None)
        if not key:
            logging.warn('KEY MISSING')
            return False

        reply = base64.b64encode(hashlib.sha1(key.encode('ascii') + self.WEBSOCK_GUID).digest()).decode('ascii')

        if len(reply) == 0:
            logging.warn('REPLY FAILED')
            return False

        logging.info('{}:{} UPGRADING CONNECTION; {}'.format(self.addr[0], self.addr[1], request_path))
        self.write('HTTP/1.1 101 Switching Protocols\r\n')
        self.write('Upgrade: WebSocket\r\n')
        self.write('Connection: Upgrade\r\n')
        self.write('Sec-WebSocket-Accept: {}\r\n\r\n'.format(reply))
        return True

    def handshakeReject(self):
        self.write('HTTP/1.1 403 Forbidden\r\n\r\n')

    def write(self, data, encode=True):
        if encode:
            data = data.encode('utf-8')
        self.socket.send(data)

    def sendMessage(self, message='', opcode=0x01):
        opcode_str = self.opcode_map[opcode] if opcode in self.opcode_map else opcode
        logging.info('{}:{} SEND: opcode: {}; length: {}; payload: "{}"'.format(self.remote_addr, self.remote_port, opcode_str, len(message), message))
        data = bytearray()
        data.append(0x80 | (opcode & 0x0F)) # FIN
        
        length = len(message)

        if length <= 125:
            data.append(length)
        elif length >= 126 and length <= 65535:
            data.append(126)
            data.extend(struct.pack("!H", length))
        else:
            data.append(127)
            data.extend(struct.pack("!Q", length))

        data.extend(message.encode('utf-8'))

        self.write(data, encode=False)

    def read(self, size):
        data = self.socket.recv(size)
        if len(data) == 0:
            self.error = True
            raise SocketClosedException
        return data

    def sockRead(self, fmt):
        length = struct.calcsize(fmt)
        data = self.read(length)
        return struct.unpack(fmt, data)[0]

    def receiveMessage(self):
        try:
            opcode = self.sockRead('B')
            flags = opcode & 0xF0
            opcode &= 0x0F
            length = self.sockRead('B')
            mask = bool(length & 0x80)
            length &= 0x7F
            if length == 126:
                length = self.sockRead('!H')
            elif length == 127:
                length = self.sockRead('!Q')
            masking_key = None
            if mask:
                masking_key = self.read(4)
            payload = ''
            if length > 0:
                payload = self.read(length)
            if masking_key is not None:
                payload2 = bytearray()
                for i in range(len(payload)):
                    payload2.append(payload[i] ^ masking_key[i % 4])
                payload = payload2
            
            opcode_str = opcode
            if opcode in self.opcode_map:
                opcode_str = self.opcode_map[opcode]
                if opcode == self.OPCODE_CLOSE:
                    if len(payload) > 0:
                        status_code = struct.unpack('!H', payload)[0]
                    else:
                        status_code = 1005
                    payload = status_code
                elif opcode != self.OPCODE_BINARY:
                    try:
                        payload = payload.decode('utf-8')
                    except UnicodeDecodeError:
                        pass
            logging.info('{}:{} RECV: opcode: {}; length: {}; payload: "{}"'.format(self.remote_addr, self.remote_port, opcode_str, length, payload))

            if opcode == self.OPCODE_CLOSE:
                raise SocketClosedException

            return opcode, payload
        except SocketClosedException:
            self.error = True
            self.socket.close()
            return False


    def close(self):
        self.socket.close()


class WebSocketServer(threading.Thread):
    def __init__(self, monitors, ssl=False):
        super().__init__()

        self._stop_event = threading.Event()

        self.monitors = monitors
        for monitor in self.monitors:
            monitor.set_server(self)
            monitor.start()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ssl:
            self.sock = ssl.wrap_socket(self.sock, server_side=True, certfile='bar.pem', keyfile='bar.pem')
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', 1234))
        self.sock.listen(0)

        self.conn = []

        # self.listen()

    def run(self):
        logging.info('LISTENING')
        next_ping = 0
        ping_timeout = 15
        while not self._stop_event.is_set():
            r, *_ = select.select([self.sock], [], [], 0.01)
            if self.sock in r:
                socket, addr = self.sock.accept()
                if addr[0] != '127.0.0.1':
                    socket.close()
                    logging.info('{}:{} REFUSED CONNECTION'.format(*addr))
                else:
                    logging.info('{}:{} CONNECTING'.format(*addr))
                    conn = WebSocketConnection(socket, addr)

                    if not conn.upgrade():
                        logging.info('{}:{} HANDSHAKE ERROR'.format(*addr))
                        conn.close()
                    else:
                        self.conn.append(conn)
                        conn.sendMessage(message='greetings', opcode=WebSocketConnection.OPCODE_PING)
                        next_ping = 0

            r, *_ = select.select([conn.socket for conn in self.conn], [], [], 0.01)
            for sock in r:
                conn = [conn for conn in self.conn if conn.socket == sock][0]
                msg = conn.receiveMessage()
                if msg != False:
                    opcode, payload = msg
                    if opcode == WebSocketConnection.OPCODE_TEXT:
                        conn.sendMessage(payload, WebSocketConnection.OPCODE_TEXT)
            self.cleanConnections()

            if time.time() >= next_ping:
                # self.sendAll(message='ping o\'clock', opcode=0x09)
                next_ping = time.time() + ping_timeout

            time.sleep(0.01)

    def stop(self):
        logging.info('STOP')
        for monitor in self.monitors:
            monitor.stop()
        for conn in self.conn:
            conn.sendMessage(opcode=WebSocketConnection.OPCODE_CLOSE) # opcode close
        self._stop_event.set()

    def on_message(self, message):
        self.sendAll(message)

    def sendAll(self, message='', opcode=0x01):
        for conn in self.conn:
            try:
                conn.sendMessage(message, opcode)
            except Exception as e:
                print(e)
                c.error = True
        self.cleanConnections()

    def cleanConnections(self):
        self.conn[:] = [c for c in self.conn if not c.error]

import serial
import serial.tools.list_ports
import select
import threading
import time
import pyudev

class PortDetect:
    def __init__(self): #, notify_event, vid='16c0', pid='0483'):
        # self.devices = [[vid, pid]]
        # self.notify_event = notify_event
        context = pyudev.Context()
        # monitor = pyudev.Monitor.from_netlink(context)
        # monitor.filter_by('tty')
        # self.observer = pyudev.MonitorObserver(monitor, self.on_event)
        # self.observer.start()

        for device in context.list_devices(subsystem='tty'):
            parent = device.find_parent('usb')
            if parent:
                print(parent)
                if 'idVendor' in parent.attributes and 'idProduct' in parent.attributes:
                    vid = parent.attributes['idVendor'].decode('ascii')
                    pid = parent.attributes['idProduct'].decode('ascii')
                    print(vid, pid)

        # import sys
        # sys.exit(0)

class Monitor(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.server = None
        self.buffer = b''
    def stop(self):
        self._stop_event.set()
    def set_server(self, server):
        self.server = server

    def notify(self, message):
        if self.server:
            self.server.on_message(message)


class SerialMonitor(Monitor):
    def __init__(self):
        super().__init__()
        # PortDetect()
        self.port = '/dev/ttyUSB0'
        self.serial = None
        self.reconnect()

    def detect_port(self):
        pass

    def reconnect(self):
        try:
            self.serial.close()
        except:
            pass
        try:
            # print('Connecting to {}...'.format(self.port))
            self.serial = serial.Serial(self.port, 19200, timeout = 0)
            return True
        except Exception as e:
            # print('Error in port {}: {}'.format(self.port, e))
            ports = list(serial.tools.list_ports.grep('ttyUSB'))
            curr_id = -1
            if len(ports) > 0:
                for i in range(len(ports)):
                    if ports[i][0] == self.port:
                        curr_id = i
                if curr_id >= 0:
                    curr_id += 1
                else:
                    curr_id = 0
                if curr_id >= len(ports):
                    curr_id = 0
                self.port = ports[i][0]
                # print('Changing port to {}'.format(self.port))
                return False
            else:
                pass
                # print('No ports found!')
                return False
        
    def processInput(self, data):
        try:
            data = data.decode('ascii')
        except AsciiDecodeError as e:
            print('AsciiDecodeError: {}'.format(e))
        if data[0] == '{':
            data = data[1:]
        data = data.strip()
        if len(data) == 0:
            return
        print('Data[{}]: {}'.format(len(data), data))
        old_ibutton = re.match(r'^i(\d+)b$', data)
        if old_ibutton:
            data = 'ibutton{' + old_ibutton.group(1) + '}'
        self.notify.on_message(data)
        # if data[0] == 'i' and data [-1] == 'b':
        #     ibutton = int(data[1:-1])
        #     self.window.ibutton_scanned.emit(ibutton)
        # elif len(data) > 8: # probably barcode?
        #     barcode = data
        #     self.window.barcode_scanned.emit(barcode)
        # else:
        #     print('Unknown data: {}'.format(data))

    def run( self ):
        # print('running')
        while not self._stop_event.is_set():
            try:
                r, w, e = select.select([self.serial],[],[], 0.01)
                if len(r) > 0:
                    try:
                        self.buffer += self.serial.read()
                    except serial.SerialException as e:
                        # print('serial.SerialException: ', e)
                        raise e
                        time.sleep(0.5)
                    while b'\r' in self.buffer:
                        line, self.buffer = self.buffer.split(b'\r', 1)
                        self.processInput(line.strip())
            except Exception as e:
                # print('Exception: ', repr(e))
                time.sleep(2)
                self.reconnect()
        # print('stopping')
        if self.serial:
            self.serial.close()

class ConsoleMonitor(Monitor):
    def run(self):
        while not self._stop_event.is_set():
            while sys.stdin in select.select([sys.stdin],[],[], 0.1)[0]:
                line = sys.stdin.readline().strip()
                if not line:
                    self.stop()
                    break
                self.notify(line)
            time.sleep(0.1)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.WARNING)
    serial_monitor = SerialMonitor()
    console_monitor = ConsoleMonitor()
    s = WebSocketServer([serial_monitor, console_monitor])
    try:
        s.start()
        s.join()
    except KeyboardInterrupt:
        s.stop()