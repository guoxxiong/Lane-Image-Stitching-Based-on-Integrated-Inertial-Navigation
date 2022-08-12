import sys
def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])

def hex2char(data):
    output = data.decode('hex')
    print(output)


if __name__ == "__main__":
    Hdata = "5c e9 fe ff 0d 87 01 00"
    data = hex2char(Hdata)
    print(data)