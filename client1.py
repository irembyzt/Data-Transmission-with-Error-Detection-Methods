import socket
import random
from controls import compute_control, safe_text

HOST = "127.0.0.1"
PORT_SERVER = 12000

METHODS = ["PARITY", "2DPARITY", "CRC16", "HAMMING", "CHECKSUM"]

def client1():
    text = safe_text(input("Text: "))
    method = random.choice(METHODS)
    control = compute_control(method, text)

    packet = f"{text}|{method}|{control}"

    s = socket.socket()
    s.connect((HOST, PORT_SERVER))
    s.send(packet.encode())
    s.close()

    print(f"Sent: {packet}")

if __name__ == "__main__":
    client1()
