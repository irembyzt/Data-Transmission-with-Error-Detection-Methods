import random

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
