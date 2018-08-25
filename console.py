import threading


class Console(threading.Thread):
    def __init__(self, serial):
        super().__init__()
        self.ser = serial
        self.lines = []
        self.lock = False

    def run(self):
        while True and not self.lock:
            line = self.ser.readline().decode()
            if line != '\r\n' and line != '':
                self.lines.append(line)
                print(line)
