import threading
import re
from config import *


class Console(threading.Thread):


    def __init__(self, serial):
        super().__init__()
        self.ser = serial
        self.status = 'IDLE'
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

    def consume_line(self, instruction):
        if type(instruction) == str:
            instruction = [instruction]

        for i in instruction:
            while i in self.lines:
                self.lines.remove(i)


    def _check_ring(self):
        ring_line = [line for line in self.lines if line == 'RING\r\n']
        if ring_line:
            self.consume_line(ring_line)

    def _check_caller(self):
        caller_line = [line for line in self.lines if '+CLIP:' in line]
        if caller_line:
            for l in caller_line:
                self.consume_line(caller_line)

    def _check_pick(self):
        pick = ['+CIEV: "CALL",1\r\n', 'CONNECT\r\n']
        pick_line = [line for line in self.lines if line in pick]
        if pick_line:
            self.consume_line(pick_line)

    def _check_hang(self):
        hang = ['+CIEV: "CALL",0\r\n', 'NO CARRIER\r\n']
        hang_line = [line for line in self.lines if line in hang]
        if hang_line:
            self.consume_line(hang_line)
