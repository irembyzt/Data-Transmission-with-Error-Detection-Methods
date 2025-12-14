import socket
from controls import compute_control

HOST = "127.0.0.1"
PORT_CLIENT2 = 9001

def client2():
    s = socket.socket()
    s.bind((HOST, PORT_CLIENT2))
    s.listen(1)

    conn,_ = s.accept()
    packet = conn.recv(4096).decode()
    conn.close()
    s.close()

    data, method, recv_ctrl, error_flag = packet.split("|")
    comp_ctrl = compute_control(method, data)

    print(f"Received Data : {data}")
    print(f"Method : {method}")
    print(f"Sent Check Bits : {recv_ctrl}")
    print(f"Computed Check Bits : {comp_ctrl}")

    if recv_ctrl == comp_ctrl:
        print("Status : DATA CORRECT")
    else:
        print("Status : DATA CORRUPTED")
