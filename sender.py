import socket
import random
from checks import METHODS, compute_control

HOST = "127.0.0.1"
PORT_SERVER = 9000


def safe_text(text: str) -> str:
    return text.replace("|", "/")


def client1():
    text = safe_text(input("Text: "))
    method = random.choice(METHODS)
    control = compute_control(method, text)
    packet = f"{text}|{method}|{control}"

    s = socket.socket()
    s.connect((HOST, PORT_SERVER))
    s.send(packet.encode())
    s.close()


if __name__ == "__main__":
    client1()
