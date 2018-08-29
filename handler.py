from threading import Thread
from config import *
import time


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

                if self.compare_status(RING_IN_EVENT):
                    self.ring_in_handler()
                elif self.compare_status(RING_OUT_EVENT):
                    self.ring_out_handler()
                elif self.compare_status(RING_IN_MISS_EVENT):
                    self.ring_in_miss_handler()
                elif self.compare_status(RING_OUT_MISS_EVENT):
                    self.ring_out_miss_handler()
                elif self.compare_status(RING_IN_SPEAK_EVENT):
                    self.ring_in_speak_handler()
                elif self.compare_status(RING_OUT_SPEAK_EVENT):
                    self.ring_out_speak_handler()
                elif self.compare_status(RING_IN_HANG_EVENT):
                    self.ring_in_hang_handler()
                elif self.compare_status(RING_OUT_HANG_EVENT):
                    self.ring_out_hang_handler()
                else:

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
