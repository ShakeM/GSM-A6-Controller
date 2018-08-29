from config import *
from core import GA6Core
from pdu import PDU
from console import Console
from handler import Handler
import time


class EasyA6(GA6Core):
    smsc = SMSC

    # Telephone status
    IDLE = 'IDLE'
    RING = 'RING'
    SPEAKING = 'SPEAKING'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = 'IDLE'
        self.handler = Handler(self)

        self.console = Console(self)
        self.console.start()

        self.wait(self.check_signal)
        ## self.display_caller_id()

    def send(self, recevier, content):
        self.wait(self.set_mode_pdu)

        if len(content) <= 70:
            content_len_zips = [PDU.encode(self.smsc, recevier, content)]
        else:
            content_len_zips = PDU.encode_long(self.smsc, recevier, content)

        for z in content_len_zips:
            content, code_len = z
            self.wait(self.set_msg_len, code_len)
            self.wait(self.send_msg, content)

    def call(self, num):
        self.wait(self.dial, num)

    def pick(self):
        self.wait(self.pick_up)

    def hang(self):
        self.wait(self.hang_up)

    def wait(self, foo, *args, timeout=RESPONSE_TIMEOUT):
        start_signal, finish_signal = foo(*args)

        pass_time = 0
        start = False
        while True:
            self.console.lock = True

            if not start:
                if start_signal in self.console.lines:
                    self.console.consume_line(start_signal)
                    start = True

            elif start:
                if finish_signal in self.console.lines:
                    self.console.consume_line(finish_signal)
                    break

                elif [e for e in self.console.lines if 'ERROR' in e]:
                    errors = [e for e in self.console.lines if 'ERROR' in e]
                    print('Inner log:', errors)
                    for e in errors:
                        self.console.consume_line(e)
                    break

            if pass_time > timeout:
                print('Inner log:', 'Timeout. Start is ', str(start))
                break

            self.console.lock = False
            pass_time += 0.2
            time.sleep(0.2)

        self.console.lock = False


ser = EasyA6(PORT, BAUD_RATE, timeout=READ_TIMEOUT)
