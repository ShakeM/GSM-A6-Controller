class PDUConverter:

    @classmethod
    def encode(cls, smsc, receiver, content, long=False, content_header=''):
        receiver, content = str(receiver), str(content)

        smsc_info = {
            'number_length': '08',
            'type': '91',
            'country': '68',
            'number': cls.__invert_number(smsc)
        }

        recevier_info = {
            'base_parameter': '11' if not long else '51',  # 长短信此处51
            'base_value': '00',
            'number_length': '0D',
            'number_type': '91',
            'country': '68',
            'number': cls.__invert_number(receiver),
        }

        content_info = {
            'protocol': '00',
            'coding': '08',
            'effective_period': 'FF',
            'content_length': hex(int(len(content_header + cls.to_hex(content)) / 2)).replace('0x', '').zfill(2),
            'hex_content': content_header + cls.to_hex(content)
        }

        recevier_info_len = len(''.join(recevier_info.values()))
        content_info_len = len(''.join(content_info.values()))
        code_len = int((recevier_info_len + content_info_len) / 2)

        code = ''.join(smsc_info.values()) + ''.join(recevier_info.values()) + ''.join(content_info.values())
        return code, code_len

    @classmethod
    def encode_long(cls, smsc, receiver, content):
        sub_contents = cls.split(content)
        content_header = {
            'head_length': '05',
            'type': '00',  # 长短信配置
            'remain_length': '03',
            'id': '0F',
            'count': hex(len(sub_contents)).replace('0x', '').zfill(2),
            'page': ''
        }

        result = []
        for i, content in enumerate(sub_contents):
            content_header['page'] = hex(i + 1).replace('0x', '').zfill(2)
            content_header_str = ''.join(content_header.values())
            code, code_len = cls.encode(smsc, receiver, content, long=True, content_header=content_header_str)
            result.append((code, code_len))
        return result

    @staticmethod
    def split(content):
        content = list(content)
        result = []

        n = 0
        while True:
            sub_content = content[n * 67:(n + 1) * 67]
            if sub_content:
                result.append(''.join(sub_content))
            else:
                return result
            n += 1

    @staticmethod
    def __invert_number(number):
        number = list(str(number))
        even_point = 1
        if len(number) % 2 == 1:
            number.append('F')

        for i in range(len(number)):
            if i == even_point:
                number[i], number[i - 1] = number[i - 1], number[i]
                even_point += 2

        return ''.join(number)

    @staticmethod
    def to_hex(string):

        hex_str = ""

        for i in range(0, len(string)):
            hex_str += (hex(ord(string[i])).replace('0x', '').zfill(4))

        return hex_str.upper()


if __name__ == '__main__':
    pdu = PDUConverter.encode_long('13010314500', '18516172878',
                                   'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')

    print(pdu)
