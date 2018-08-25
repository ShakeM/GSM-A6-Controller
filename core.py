import serial


class GA6Core(serial.Serial):
    def check_signal(self):
        instruction = b'AT\r\n'
        self.write(instruction)
        return instruction.decode()

    def get_sim_status(self):
        instruction = b'AT+CPIN?\r\n'
        instruction = instruction
        self.write(instruction)
        return instruction.decode()

    def get_registration(self):
        instruction = b'AT+CREG?\r\n'
        instruction = instruction
        self.write(instruction)
        return instruction.decode()

    def get_imei(self):
        instruction = b'AT+GSN\r\n'
        self.write(instruction)
        return instruction.decode()

    def get_msg_storage(self):
        instruction = b'AT+CPMS?\r\n'
        self.write(instruction)
        return instruction.decode()

    def get_msg(self, num):
        num = str(num)
        instruction = f'AT+CMGR={num}\r\n'.encode()
        self.write(instruction)
        return instruction.decode()

    def get_unread_msg(self):
        instruction = b'AT+CMGL=0\r\n'
        self.write(instruction)
        return instruction.decode()

    def get_read_msg(self):
        instruction = b'AT+CMGL=1\r\n'
        self.write(instruction)
        return instruction.decode()

    def get_draft_msg(self):
        instruction = b'AT+CMGL=2\r\n'
        self.write(instruction)
        return instruction.decode()

    def get_sent_msg(self):
        instruction = b'AT+CMGL=3\r\n'
        self.write(instruction)
        return instruction.decode()

    def get_all_msg(self):
        instruction = b'AT+CMGL=4\r\n'
        self.write(instruction)
        return instruction.decode()

    def delete_msg(self, num):
        num = str(num)
        instruction = f'AT+CMGD={num}\r\n'.encode()
        self.write(instruction)
        return instruction.decode()

    def delete_read_msg(self):
        instruction = f'AT+CMGD=1,1\r\n'.encode()
        self.write(instruction)
        return instruction.decode()

    def delete_read_sent_msg(self):
        instruction = f'AT+CMGD=1,2\r\n'.encode()
        self.write(instruction)
        return instruction.decode()

    def delete_read_sent_unsend_msg(self):
        instruction = f'AT+CMGD=1,3\r\n'.encode()
        self.write(instruction)
        return instruction.decode()

    def delete_all_msg(self):
        instruction = f'AT+CMGD=1,4\r\n'.encode()
        self.write(instruction)
        return instruction.decode()

    def dial(self, num):
        num = str(num)
        instruction = f'ATD{num}\r\n'.encode()
        self.write(instruction)
        return instruction.decode()

    def pick_up(self):
        instruction = b'ATA\r\n'
        self.write(instruction)
        return instruction.decode()

    def hang_up(self):
        instruction = b'ATH\r\n'
        self.write(instruction)
        return instruction.decode()

    def redial(self):
        instruction = b'AT+DLST\r\n'
        self.write(instruction)
        return instruction.decode()

    def display_caller_id(self):
        instruction = b'AT+CLIP=1\r\n'
        self.write(instruction)
        return instruction.decode()

    def conceal_caller_id(self):
        instruction = b'AT+CLIP=0\r\n'
        self.write(instruction)
        return instruction.decode()

    def shift_headset(self):
        instruction = b'AT+SNFS=1\r\n'
        self.write(instruction)
        return instruction.decode()

    def shift_horn(self):
        instruction = b'AT+SNFS=0\r\n'
        self.write(instruction)
        return instruction.decode()

    def set_mode_text(self):
        instruction = b'AT+CMGF=1\r\n'
        self.write(instruction)
        return instruction.decode()

    def set_mode_pdu(self):
        instruction = b'AT+CMGF=0\r\n'
        self.write(instruction)
        return instruction.decode()

    def set_charset_gsm(self):
        instruction = b'AT+CSCS="GSM"\r\n'
        self.write(instruction)
        return instruction.decode()

    def set_msg_target(self, num):
        instruction = f'AT+CMGS="{num}"\r\n'.encode()
        self.write(instruction)
        return instruction.decode()

    def set_msg_len(self, num):
        num = str(num)
        instruction = f'AT+CMGS={num}\r\n'.encode()
        self.write(instruction)
        return instruction.decode()

    # SM,ME,MT
    def set_msg_storage(self, mem1, mem2, mem3):
        instruction = f'AT+CPMS="{mem1}","{mem2}","{mem3}"\r\n'.encode()
        self.write(instruction)
        return instruction.decode()

    def set_msg_content(self, content):
        content = str(content)
        instruction = content.encode()
        self.write(instruction)
        return instruction.decode()

    def send_msg(self):
        instruction = b'\x1A'
        self.write(instruction)
        return instruction.decode()
