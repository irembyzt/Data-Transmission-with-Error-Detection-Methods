import socket
import random
from errors import ERROR_METHODS

HOST = "127.0.0.1"
PORT_SERVER = 9000
PORT_CLIENT2 = 9001

def server():
    s = socket.socket()
    s.bind((HOST, PORT_SERVER))
    s.listen(1)

    conn,_ = s.accept()
    packet = conn.recv(4096).decode()
    conn.close()
    s.close()

    data, method, control = packet.split("|")

    error_name, error_func = random.choice(list(ERROR_METHODS.items()))
    corrupted = data if error_func is None else error_func(data)

    fwd = socket.socket()
    fwd.connect((HOST, PORT_CLIENT2))
    error_flag = "1" if error_name != "NO ERROR" else "0"
    fwd.send(f"{corrupted}|{method}|{control}|{error_flag}".encode())
    fwd.close()
