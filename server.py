import socket
from controls import ERROR_METHODS

HOST = "127.0.0.1"
PORT_SERVER = 12000
PORT_CLIENT2 = 12001


# Method -> Error mapping (akademik olarak doğru)
METHOD_ERROR_MAP = {
    "PARITY": ("Multiple Bit Flips", ERROR_METHODS["Multiple Bit Flips"]),
    "2DPARITY": ("Burst Error", ERROR_METHODS["Burst Error"]),
    "CRC16": ("Burst Error", ERROR_METHODS["Burst Error"]),
    "HAMMING": ("Bit Flip", ERROR_METHODS["Bit Flip"]),
    "CHECKSUM": ("Character Substitution", ERROR_METHODS["Character Substitution"]),
}


def server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT_SERVER))
    s.listen(5)

    print("DATACOM SERVER STARTED")

    while True:
        conn, addr = s.accept()
        packet = conn.recv(4096).decode()
        conn.close()

        # DATA | METHOD | CONTROL
        data, method, control = packet.split("|", 2)

        error_name, error_func = METHOD_ERROR_MAP.get(method, ("NO ERROR", None))
        corrupted = data if error_func is None else error_func(data)
        error_flag = "1" if error_func else "0"

        print("----------------------------------")
        print(f"[SERVER] Method     : {method}")
        print(f"[SERVER] Error Type : {error_name}")
        print(f"[SERVER] Original   : {data}")
        print(f"[SERVER] Corrupted  : {corrupted}")
        print("----------------------------------")

        fwd = socket.socket()
        fwd.connect((HOST, PORT_CLIENT2))
        fwd.send(f"{corrupted}|{method}|{control}|{error_flag}".encode())
        fwd.close()


if __name__ == "__main__":
    server()
