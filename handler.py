from threading import Thread
from config import *
import time

RING_IN = [RING_IN, IDLE]
RING_OUT = [RING_OUT, IDLE]
RING_IN_MISS = [IDLE, RING_IN]
RING_OUT_MISS = [IDLE, RING_OUT]
RING_IN_SPEAK = [SPEAKING, RING_IN]
RING_OUT_SPEAK = [SPEAKING, RING_OUT]
RING_IN_HANG = [IDLE, SPEAKING, RING_IN]
RING_OUT_HANG = [IDLE, SPEAKING, RING_OUT]


class Handler(Thread):
    def __init__(self, serial):
        super().__init__()
        self.ser = serial
        self.status_heap = [None for _ in range(3)]

    def run(self):
        while True:
            if self.status_heap[0] == self.ser.status:
                pass
            else:
                self.push_new_status(self.ser.status)

                if self.compare_status(RING_IN):
                    self.ring_in_handler()
                elif self.compare_status(RING_OUT):
                    self.ring_out_handler()
                elif self.compare_status(RING_IN_MISS):
                    self.ring_in_miss_handler()
                elif self.compare_status(RING_OUT_MISS):
                    self.ring_out_miss_handler()
                elif self.compare_status(RING_IN_SPEAK):
                    self.ring_in_speak_handler()
                elif self.compare_status(RING_OUT_SPEAK):
                    self.ring_out_speak_handler()
                elif self.compare_status(RING_IN_HANG):
                    self.ring_in_hang_handler()
                elif self.compare_status(RING_OUT_HANG):
                    self.ring_out_hang_handler()

    def push_new_status(self, status):
        self.status_heap.insert(0, status)
        self.status_heap.pop()

    def compare_status(self, model):
        for i in range(len(model)):
            if model[i] == self.status_heap[i]:
                continue
            else:
                return False
        return True

    def ring_in_handler(self):
        print("ring_in_handler")
        pass

    def ring_out_handler(self):
        print('ring_out_handler')
        pass

    def ring_in_miss_handler(self):
        print('ring_in_miss_handler')
        pass

    def ring_out_miss_handler(self):
        print('ring_out_miss_handler')
        pass

    def ring_in_speak_handler(self):
        print('ring_in_speak_handler')
        pass

    def ring_out_speak_handler(self):
        print('ring_out_speak_handler')
        pass

    def ring_in_hang_handler(self):
        print('ring_in_hang_handler')
        pass

    def ring_out_hang_handler(self):
        print('ring_out_hang_handler')
        pass

    def new_msg_handler(self):
        print('new_msg_handler')
        pass

    def caller_handler(self):
        print('caller_handler')
        pass
