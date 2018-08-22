import binascii


class PDUConverter:

    # 上海联通中心号码SMSC 13010314500
    @classmethod
    def encode(cls, smsc, receiver, content):
        smsc_info = {
            'address_length': '08',
            'type': '91',
            'country': '68',
            'number': cls.__invert_number(smsc)
        }

        recevier_info = {
            'base_parameter': '11',
            'base_value': '00',
            'address_length': '0D',
            'type': '91',
            'nation': '68',
            'number': cls.__invert_number(receiver),
        }

        content_info = {
            'protocol': '00',
            'charset': '08',
            'effective_period': 'FF',
            'content_length': hex(int(len(str(content.encode('unicode-escape'))
                                          .replace('\\\\u', '').replace("b'", '')
                                          .replace("'", '')) / 2)).replace('0x', '').zfill(2),
            'hex_content': str(content.encode('unicode-escape'))
                .replace('\\\\u', '').replace("b'", '').replace("'", '').upper(),

        }

        return ''.join(smsc_info.values()) + ''.join(recevier_info.values()) + ''.join(content_info.values())

    @staticmethod
    def __invert_number(number):
        even_point = 1
        number = list(number)
        if len(number) % 2 == 1:
            number.append('F')

        for i in range(len(number)):
            if i == even_point:
                number[i], number[i - 1] = number[i - 1], number[i]
                even_point += 2

        return ''.join(number)


if __name__ == '__main__':
    pdu = PDUConverter.encode('13010314500', '18516172878', '哈哈哈')
    print(pdu)