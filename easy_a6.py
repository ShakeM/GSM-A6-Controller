from config import *
from core import GA6Core
from pdu_converter import PDUConverter
from console import Console


class EasyA6(GA6Core):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_signal()
        self.display_caller_id()
        self.smsc = SMSC
        self.record = []

    def send(self, recevier, content):
        self.set_mode_pdu()
        content, code_len = PDUConverter.encode(self.smsc, str(recevier), str(content))
        self.set_msg_len(str(code_len))
        self.set_msg_content(content.encode())
        self.send_msg()


ser = EasyA6(PORT, BAUD_RATE, timeout=TIMEOUT)

reader = Console(ser)
reader.start()
