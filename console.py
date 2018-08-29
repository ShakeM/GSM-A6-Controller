import threading
import re
from config import *


class Console(threading.Thread):

    def __init__(self, serial):
        super().__init__()
        self.ser = serial
        self.lines = []
        self.lock = False

    def run(self, output=True):
        while True:
            if not self.lock:
                line = self.ser.readline().decode()
                if line != '\r\n' and line != '':
                    self.lines.append(line)
                    if output:
                        print(line)
                self.ser.status = self.get_status()
                self.ser.caller = self.get_caller()

    def consume_line(self, instruction):
        if type(instruction) == str:
            instruction = [instruction]

        for i in instruction:
            while i in self.lines:
                self.lines.remove(i)

    def get_status(self):
        if self._check_ring_in():
            return RING_IN
        elif self._check_pick():
            return SPEAKING
        elif self._check_hang():
            return IDLE

    def get_caller(self):
        phone_number = self._check_caller().replace('+CLIP: ', '')
        return phone_number

    def _check_ring_in(self):
        ring_line = [line for line in self.lines if line == 'RING\r\n']
        if ring_line:
            self.consume_line(ring_line)
            return True
        else:
            return False

    def _check_ring_out(self):
        ring_out = ['+CIEV: "SOUNDER",1\r\n', '+CIEV: "SOUNDER",0\r\n']
        ring_line = [line for line in self.lines if line in ring_out]
        if ring_line:
            self.consume_line(ring_line)
            return True
        else:
            return False

    def _check_pick(self):
        pick = ['+CIEV: "CALL",1\r\n', 'CONNECT\r\n']
        pick_line = [line for line in self.lines if line in pick]
        if pick_line:
            self.consume_line(pick_line)
            return True
        else:
            return False

    def _check_hang(self):
        hang = ['+CIEV: "CALL",0\r\n', 'NO CARRIER\r\n']
        hang_line = [line for line in self.lines if line in hang]
        if hang_line:
            self.consume_line(hang_line)
            return True
        else:
            return False

    def _check_caller(self):
        caller_line = [line for line in self.lines if '+CLIP:' in line]
        if caller_line:
            for l in caller_line:
                self.consume_line(l)
                return l
