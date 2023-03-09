from machine import UART, Pin
from os import uname
import time
import binascii

class nextion:
    WRITE_ONLY = 0
    WRITE_AND_READ = 1
    DECODE = 1
    RAW = 0
    def __init__(self, tx_pin, rx_pin, baudrate):
        self.uart = UART(0, baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.uart.init(baudrate, bits=8, parity=None, stop=1)
    def cmd(self, cmd, flags=WRITE_AND_READ):
        end_cmd=b'\xFF\xFF\xFF'
        self.uart.write(cmd)
        self.uart.write(end_cmd)
        if(flags == 1):
            time.sleep_ms(100)
            return self.uart.read()
    def sleep(self, state):
        self.cmd("sleep=" + str(state))
    def page(self, page):
        self.cmd("page " + str(page))
    def reset(self):
        self.cmd("rest")
    def brightness(self, brightness):
        self.cmd("dim=" + str(brightness))
    def write_text(self, id_text, text):
        self.cmd(id_text + '='+ '"' + str(text) + '"')  
    def read(self, flags=1):
        if(flags == 0):
            return self.uart.read()
        else:
            output = self.uart.read()
            if(not output is None):
                #output.replace("\xFF\xFF\xFF", "")
                #output = bytearray(str(output)).decode("ascii")
                #output1 = bytearray(str(output), encoding="utf-8")
                #output.decode("ascii")
                output1 = binascii.hexlify(output).decode('ascii')
                print(output1)
                try:
                    from_nextion = [int(output1[0:2]), int(output1[2:4], 16), int(output1[4:6], 16)]
                except:
                    return output1
                return from_nextion
            else:
                return None
