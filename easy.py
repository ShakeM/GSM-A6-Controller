from config import *
from g import *
from core import GA6Core
from pdu import PDU
from line_buffer import LineBuffer
# from event_handler import EventHandler
import time

__all__ = ['EasyGSM']


class EasyGSM:

    def __init__(self, core_cls, smsc, *args,
                 line_buffer_cls=LineBuffer,
                 # event_handler_cls=EventHandler,
                 **kwargs):
        self.core = core_cls(*args, **kwargs)
        self.smsc = smsc

        self.status_heap = [None, None, None]
        self.caller = ''

        self.buffer = line_buffer_cls(self.core, self.status_heap)
        self.buffer.start()

        # self.handler = event_handler_cls(self)
        # self.handler.start()

        self.wait(core_cls.check_wire)
        ## self.display_caller_id()

    def send(self, recevier, content):
        self.wait(self.core.set_mode_pdu)

        if len(content) <= 70:
            content_len_zips = [PDU.encode(self.smsc, recevier, content)]
        else:
            content_len_zips = PDU.encode_long(self.smsc, recevier, content)

        for z in content_len_zips:
            content, code_len = z
            self.wait(self.core.set_msg_len, code_len)
            self.wait(self.core.send_msg, content)

    def call(self, num):
        self.wait(self.core.dial, num)

    def pick(self):
        self.wait(self.core.pick_up)

    def hang(self):
        self.wait(self.core.hang_up)

    def wait(self, foo, *args, timeout=RESPONSE_TIMEOUT):
        start_signal, finish_signal = foo(*args)

        pass_time = 0
        start = False
        while True:
            self.buffer.lock = True

            if not start:
                if start_signal in self.buffer.lines:
                    self.buffer.consume_line(start_signal)
                    start = True

            elif start:
                if not finish_signal:
                    break
                elif finish_signal in self.buffer.lines:
                    self.buffer.consume_line(finish_signal)
                    break
                elif [e for e in self.buffer.lines if 'ERROR' in e]:
                    errors = [e for e in self.buffer.lines if 'ERROR' in e]
                    print('Inner log:', errors)
                    for e in errors:
                        self.buffer.consume_line(e)
                    break

            if pass_time > timeout:
                print('Inner log:', 'Timeout. Start is ', str(start))
                break

            self.buffer.lock = False
            pass_time += 0.2
            time.sleep(0.2)

        self.buffer.lock = False


ser = EasyGSM(GA6Core, SMSC, PORT, BAUD_RATE, timeout=READ_TIMEOUT)
