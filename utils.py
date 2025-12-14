def bytes_to_bitstr(b: bytes) -> str:
    return "".join(f"{byte:08b}" for byte in b)

def bitstr_to_hex(bitstr: str) -> str:
    if len(bitstr) % 4 != 0:
        bitstr += "0" * (4 - len(bitstr) % 4)
    return "".join(f"{int(bitstr[i:i+4], 2):X}" for i in range(0, len(bitstr), 4))

def safe_text(text: str) -> str:
    return text.replace("|", "/")
