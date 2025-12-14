import socket
import random
from controls import compute_control, METHODS

HOST = "127.0.0.1"
PORT_SERVER = 9000

def client1(text):
    method = random.choice(METHODS)
    control = compute_control(method, text)
    packet = f"{text}|{method}|{control}"

    s = socket.socket()
    s.connect((HOST, PORT_SERVER))
    s.send(packet.encode())
    s.close()
