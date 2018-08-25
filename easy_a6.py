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

        self.status = IDLE
        self.caller = ''

        self.wait(self.check_signal)
        ## self.display_caller_id()

    def send(self, recevier, content):
        self.wait(self.set_mode_pdu)
        content, code_len = PDUConverter.encode(self.smsc, recevier, content)
        self.wait(self.set_msg_len, code_len, response='> ')
        self.wait(self.set_msg_content, content, response=None)
        self.wait(self.send_msg, ignore='+CMGS: 0\r\n')

    def pick(self):
        self.wait(self.pick_up)

    def wait(self, foo, *args, response='OK\r\n', ignore='', timeout=RESPONSE_TIMEOUT):
        result = foo(*args)

        pass_time = 0
        sent = False
        while True:
            if result in self.console.lines and not sent:
                sent = True
                self._consume_line(result)
            if ignore in self.console.lines:
                self._consume_line(ignore)

            if not response:
                break
            if response in self.console.lines and sent:
                self._consume_line(response)
                break
            elif [e for e in self.console.lines if 'ERROR' in e]:
                errors = [e for e in self.console.lines if 'ERROR' in e]
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
        if type(instruction) == str:
            instruction = [instruction]

        for i in instruction:
            while i in self.console.lines:
                self.console.lines.remove(i)

    def update_status(self):
        self.console.lock = True

        ring_line = [line for line in self.console.lines if line == 'RING\r\n']
        if ring_line:
            self.status = RING
            self._consume_line(ring_line)

        caller_line = [line for line in self.console.lines if '+CLIP:' in line]
        if caller_line:
            for l in caller_line:
                re_result = re.search('(?<=").*?(?=")', l)
                self.caller = re_result[0] if re_result else ''
                self._consume_line(caller_line)

        talk = ['+CIEV: "CALL",1\r\n', 'CONNECT\r\n']
        talk_line = [line for line in self.console.lines if line in talk]
        if talk_line:
            self.status = TALK
            self._consume_line(talk_line)

        stop = ['+CIEV: "CALL",0\r\n', 'NO CARRIER\r\n']
        stop_line = [line for line in self.console.lines if line in stop]
        if stop_line:
            self.status = IDLE
            self._consume_line(stop_line)

        self.console.lock = False
        return self.status


ser = EasyA6(PORT, BAUD_RATE, timeout=READ_TIMEOUT)
