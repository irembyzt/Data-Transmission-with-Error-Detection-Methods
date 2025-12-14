from utils import bytes_to_bitstr, bitstr_to_hex

METHODS = ["PARITY", "2DPARITY", "CRC16", "HAMMING", "CHECKSUM"]

def parity_control(text: str) -> str:
    bits = bytes_to_bitstr(text.encode())
    return "0" if bits.count("1") % 2 == 0 else "1"

def parity2d_control(text: str, cols=8) -> str:
    bits = bytes_to_bitstr(text.encode())
    rows = (len(bits) + cols - 1) // cols
    bits = bits.ljust(rows * cols, "0")
    matrix = [bits[i*cols:(i+1)*cols] for i in range(rows)]

    row_p = ["0" if r.count("1") % 2 == 0 else "1" for r in matrix]
    col_p = []
    for c in range(cols):
        ones = sum(1 for r in matrix if r[c] == "1")
        col_p.append("0" if ones % 2 == 0 else "1")

    return "".join(row_p) + "," + "".join(col_p)

def crc16(text: str) -> str:
    crc = 0xFFFF
    for b in text.encode():
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) if crc & 0x8000 else crc << 1
            crc &= 0xFFFF
    return f"{crc:04X}"

def checksum(text: str) -> str:
    data = text.encode()
    if len(data) % 2:
        data += b"\x00"
    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i+1]
        s = (s & 0xFFFF) + (s >> 16)
    return f"{(~s) & 0xFFFF:04X}"

def hamming_control(text: str) -> str:
    bits = bytes_to_bitstr(text.encode())
    bits = bits.ljust(len(bits) + (-len(bits) % 4), "0")

    def encode4(b):
        d1,d2,d3,d4 = map(int, b)
        p1 = d1 ^ d2 ^ d4
        p2 = d1 ^ d3 ^ d4
        p4 = d2 ^ d3 ^ d4
        return f"{p1}{p2}{d1}{p4}{d2}{d3}{d4}"

    encoded = "".join(encode4(bits[i:i+4]) for i in range(0, len(bits), 4))
    return bitstr_to_hex(encoded)

def compute_control(method, data):
    return {
        "PARITY": parity_control,
        "2DPARITY": parity2d_control,
        "CRC16": crc16,
        "HAMMING": hamming_control,
        "CHECKSUM": checksum
    }[method](data)
