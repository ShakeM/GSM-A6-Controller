from config import *
from core import GA6Core
from pdu_converter import PDUConverter
from console import Console
import time


class EasyA6(GA6Core):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console(self)
        self.console.start()

        self.wait(self.check_signal)
        # self.display_caller_id()
        self.smsc = SMSC

    def send(self, recevier, content):
        self.set_mode_pdu()
        content, code_len = PDUConverter.encode(self.smsc, str(recevier), str(content))
        self.set_msg_len(str(code_len))
        self.set_msg_content(content.encode())
        self.send_msg()

    def wait(self, foo, timeout=RESPONSE_TIMEOUT):
        result = foo()

        pass_time = 0
        sent = False
        while True:
            if result in self.console.lines and sent == False:
                print(result)
                sent = True
            elif 'OK\r\n' in result and sent == True:
                print('Done')
                break
            elif [e for e in result if 'ERROR:' in e]:
                print([e for e in result if 'ERROR:' in e])
                break
            elif pass_time > timeout:
                print('Timeout')
                break

            pass_time += 0.2
            time.sleep(0.2)


ser = EasyA6(PORT, BAUD_RATE, timeout=READ_TIMEOUT)
