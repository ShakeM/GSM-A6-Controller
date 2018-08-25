from config import *
from core import GA6Core
from pdu_converter import PDUConverter
from console import Console
import time
import re


class EasyA6(GA6Core):
    smsc = SMSC

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console(self)
        self.console.start()

        self.wait(self.check_signal)
        self.ring = False
        self.caller = ''
        ## self.display_caller_id()

    def send(self, recevier, content):
        self.set_mode_pdu()
        content, code_len = PDUConverter.encode(self.smsc, recevier, content)
        self.set_msg_len(code_len)
        self.set_msg_content(content)
        self.send_msg()

    def wait(self, foo, timeout=RESPONSE_TIMEOUT):
        result = foo()

        pass_time = 0
        sent = False
        while True:
            if result in self.console.lines and not sent:
                sent = True
            elif 'OK\r\n' in self.console.lines and sent:
                self._consume_line('OK\r\n')
                break
            elif [e for e in self.console.lines if 'ERROR:' in e]:
                errors = [e for e in self.console.lines if 'ERROR:' in e]
                print('Inner log:', errors)
                for e in errors:
                    self._consume_line(e)
                break
            elif pass_time > timeout:
                print('Inner log:', 'Timeout')
                break

            pass_time += 0.2
            time.sleep(0.2)

    def _consume_line(self, instruction):
        self.console.lock = True

        if type(instruction) == str:
            instruction = [instruction]

        for i in instruction:
            while i in self.console.lines:
                self.console.lines.remove(i)

        self.console.lock = False

    def check_ring(self):
        ring_line = [line for line in self.console.lines if line == 'RING\r\n']
        if ring_line:
            self.ring = True
            self._consume_line(ring_line)

        caller_line = [line for line in self.console.lines if '+CLIP:' in line]
        if caller_line:
            re_result = re.search('(?<=").*?(?=")', caller_line)
            self.caller = re_result[0] if re_result else ''
            self._consume_line(caller_line)

        stop = ['+CIEV:"CALL",0\r\n', 'NO CARRIER\r\n']
        stop_line = [line for line in self.console.lines if line in stop]
        if stop_line:
            self.ring = False
            self._consume_line(stop_line)


ser = EasyA6(PORT, BAUD_RATE, timeout=READ_TIMEOUT)
