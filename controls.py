import random

# =========================
# Utility
# =========================
def bytes_to_bitstr(b: bytes) -> str:
    return "".join(f"{byte:08b}" for byte in b)

def bitstr_to_hex(bitstr: str) -> str:
    if len(bitstr) % 4 != 0:
        bitstr += "0" * (4 - len(bitstr) % 4)
    return "".join(f"{int(bitstr[i:i+4], 2):X}" for i in range(0, len(bitstr), 4))

def safe_text(text: str) -> str:
    return text.replace("|", "/")

# =========================
# Control Methods
# =========================
def parity_control(text):
    bits = bytes_to_bitstr(text.encode())
    return "0" if bits.count("1") % 2 == 0 else "1"

def parity2d_control(text, cols=8):
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

def crc16(text):
    crc = 0xFFFF
    for b in text.encode():
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) if crc & 0x8000 else crc << 1
            crc &= 0xFFFF
    return f"{crc:04X}"

def checksum(text):
    data = text.encode()
    if len(data) % 2:
        data += b"\x00"
    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i+1]
        s = (s & 0xFFFF) + (s >> 16)
    return f"{(~s) & 0xFFFF:04X}"

def hamming_control(text):
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

# =========================
# Error Injection
# =========================
def bit_flip(text):
    b = bytearray(text.encode())
    i = random.randrange(len(b))
    b[i] ^= 1 << random.randrange(8)
    return b.decode(errors="replace")

def char_sub(text):
    i = random.randrange(len(text))
    return text[:i] + chr(random.randint(32,126)) + text[i+1:]

def char_del(text):
    i = random.randrange(len(text))
    return text[:i] + text[i+1:]

def char_ins(text):
    i = random.randrange(len(text)+1)
    return text[:i] + chr(random.randint(32,126)) + text[i:]

def char_swap(text):
    i = random.randrange(len(text)-1)
    return text[:i] + text[i+1] + text[i] + text[i+2:]

def multi_bit(text):
    for _ in range(3):
        text = bit_flip(text)
    return text

def burst(text):
    n = random.randint(3, min(8, len(text)))
    i = random.randint(0, len(text)-n)
    return text[:i] + "".join(chr(random.randint(32,126)) for _ in range(n)) + text[i+n:]

ERROR_METHODS = {
    "NO ERROR": None,
    "Bit Flip": bit_flip,
    "Character Substitution": char_sub,
    "Character Deletion": char_del,
    "Random Insertion": char_ins,
    "Character Swap": char_swap,
    "Multiple Bit Flips": multi_bit,
    "Burst Error": burst
}
