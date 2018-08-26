class PDUConverter:

    # 上海联通中心号码SMSC 13010314500
    @classmethod
    def encode(cls, smsc, receiver, content):
        receiver, content = str(receiver), str(content)
        if len(content) > 70:
            content = cls.split(content)


        smsc_info = {
            'number_length': '08',
            'type': '91',
            'country': '68',
            'number': cls.__invert_number(smsc)
        }

        recevier_info = {
            'base_parameter': '11',
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
            'content_length': hex(int(len(cls.to_hex(content)) / 2)).replace('0x', '').zfill(2),
            'hex_content': cls.to_hex(content)
        }

        hex_content_head = {
            'head_length': '05',
            'type': '00',  # 长短信配置
            'remain_length': '03',
            'id': '',
            'count': '',
            'page': ''
        }

        recevier_info_len = len(''.join(recevier_info.values()))
        content_info_len = len(''.join(content_info.values()))
        code_len = int((recevier_info_len + content_info_len) / 2)

        code = ''.join(smsc_info.values()) + ''.join(recevier_info.values()) + ''.join(content_info.values())
        return code, code_len

    @staticmethod
    def split(content):
        content = list(content)
        result = []

        n = 0
        while True:
            sub_content = content[n * 67:(n + 1) * 67]
            if sub_content:
                result.append(sub_content)
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
    pdu = PDUConverter.encode('13010314500', '18516172878',
                              'a你好我好大家好好大家好你好我好大家好你好我好大家好你好我好大家好你好我好大家好你好我好大家好你好我好大家好你好我好大家好')
    pdu = PDUConverter.split('哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈')
    print(pdu)
