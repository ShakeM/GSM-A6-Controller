import threading


class Console(threading.Thread):
    def __init__(self, serial):
        super().__init__()
        self.ser = serial
        self.lines = []

    def run(self):
        while True:
            line = self.ser.readline().decode()
            if line != '\r\n' and line != '':
                self.lines.append(line)
