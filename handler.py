from threading import Thread


class Handler(Thread):
    def __init__(self, serial):
        super().__init__()
        self.ser = serial

    def run(self):
        # while True:
        #     pass
        pass

    def ring_handler(self):
        pass

    def caller_handler(self):
        pass

    def pick_handler(self):
        pass

    def hang_handler(self):
        pass

    def new_msg_handler(self):
        pass
