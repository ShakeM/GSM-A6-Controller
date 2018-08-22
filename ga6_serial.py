import serial
from config import *
import threading


class GA6Serial(serial.Serial):
    def check_serial(self):
        self.write(b'AT\r\n')

    def get_sim(self):
        self.write(b'AT+CPIN?\r\n')

    def get_registration(self):
        self.write(b'AT+CREG?\r\n')

    def get_imei(self):
        self.write(b'AT+GSN\r\n')

    def get_msg_storage(self):
        self.write(b'AT+CPMS?\r\n')

    def get_msg(self, num):
        num = str(num)
        self.write(f'AT+CMGR={num}\r\n'.encode())

    def delete_msg(self, num):
        num = str(num)
        self.write(f'AT+CMGD={num}\r\n'.encode())

    def delete_read_msg(self):
        self.write(f'AT+CMGD=1,1\r\n'.encode())

    def delete_read_sent_msg(self):
        self.write(f'AT+CMGD=1,2\r\n'.encode())

    def delete_read_sent_unsend_msg(self):
        self.write(f'AT+CMGD=1,3\r\n'.encode())

    def delete_all_msg(self):
        self.write(f'AT+CMGD=1,4\r\n'.encode())

    def dial(self, num):
        num = str(num)
        self.write(f'ATD{num}\r\n'.encode())

    def pick_up(self):
        self.write(b'ATA\r\n')

    def hang_up(self):
        self.write(b'ATH\r\n')

    def redial(self):
        self.write(b'AT+DLST\r\n')

    def display_caller_id(self):
        self.write(b'AT+CLIP=1\r\n')

    def conceal_caller_id(self):
        self.write(b'AT+CLIP=0\r\n')

    def shift_headset(self):
        self.write(b'AT+SNFS=1\r\n')

    def shift_horn(self):
        self.write(b'AT+SNFS=0\r\n')

    def set_mode_text(self):
        self.write(b'AT+CMGF=1\r\n')

    def set_mode_pdu(self):
        self.write(b'AT+CMGF=0\r\n')

    def set_charset_gsm(self):
        self.write(b'AT+CSCS="GSM"\r\n')

    def set_msg_target(self, num):
        self.write(f'AT+CMGS="{num}"\r\n'.encode())

    def set_msg_length(self, num):
        num = str(num)
        self.write(f'AT+CMGS={num}\r\n'.encode())

    # SM,ME,MT
    def set_msg_storage(self, mem1, mem2, mem3):
        self.write(f'AT+CPMS="{mem1}","{mem2}","{mem3}"\r\n'.encode())

    def set_msg_content(self, content):
        content = str(content)
        self.write(content.encode())

    def send_msg(self):
        self.write(b'\x1A')


ser = GA6Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
