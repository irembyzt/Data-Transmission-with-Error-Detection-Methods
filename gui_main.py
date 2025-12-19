import tkinter as tk
from tkinter import ttk
import socket
import threading
from controls import compute_control, safe_text

# =====================
# CONFIG
# =====================
HOST = "127.0.0.1"
PORT_SERVER = 12000
PORT_CLIENT2 = 12001

METHODS = ["PARITY", "2DPARITY", "CRC16", "HAMMING", "CHECKSUM"]

BG = "#000000"
FG = "#00FF00"
FONT = ("Consolas", 10)

METHOD_INFO = {
    "PARITY": "Parity may fail for even number of bit errors",
    "2DPARITY": "2D parity detects many burst errors",
    "CRC16": "CRC is strong against burst errors",
    "HAMMING": "Hamming detects single-bit errors",
    "CHECKSUM": "Checksum provides weak error detection"
}


class DataComGUI:
    def __init__(self, root):
        root.title("DATACOM :: Error Control Simulator")
        root.geometry("1150x650")
        root.configure(bg=BG)

        # ===== STYLE (HACKER COMBOBOX) =====
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Hacker.TCombobox",
            fieldbackground=BG,
            background=BG,
            foreground=FG,
            arrowcolor=FG,
            bordercolor=FG
        )
        style.map(
            "Hacker.TCombobox",
            fieldbackground=[("readonly", BG)],
            foreground=[("readonly", FG)],
            background=[("readonly", BG)]
        )

        # ===== HEADER =====
        tk.Label(
            root,
            text=">> DATACOM ERROR CONTROL TERMINAL <<",
            bg=BG, fg=FG,
            font=("Consolas", 14, "bold")
        ).pack(pady=10)

        # ===== INPUT AREA =====
        top = tk.Frame(root, bg=BG)
        top.pack(pady=5)

        tk.Label(top, text="TEXT >", bg=BG, fg=FG, font=FONT).pack(side=tk.LEFT)
        self.entry = tk.Entry(
            top, width=35,
            bg=BG, fg=FG,
            insertbackground=FG,
            font=FONT,
            relief=tk.FLAT
        )
        self.entry.pack(side=tk.LEFT, padx=10)

        tk.Label(top, text="METHOD >", bg=BG, fg=FG, font=FONT).pack(side=tk.LEFT)

        self.method_box = ttk.Combobox(
            top,
            values=METHODS,
            state="readonly",
            width=12,
            style="Hacker.TCombobox"
        )
        self.method_box.current(0)
        self.method_box.pack(side=tk.LEFT, padx=10)

        tk.Button(
            top,
            text="[ SEND ]",
            bg=BG, fg=FG,
            font=FONT,
            relief=tk.FLAT,
            activebackground="#003300",
            command=lambda: threading.Thread(
                target=self.run_simulation, daemon=True
            ).start()
        ).pack(side=tk.LEFT)

        # ===== PANELS =====
        panels = tk.Frame(root, bg=BG)
        panels.pack(pady=15)

        self.client1_box = self.make_panel(panels, "CLIENT 1 (SENDER)")
        self.server_box  = self.make_panel(panels, "SERVER (ERROR INJECTOR)")
        self.client2_box = self.make_panel(panels, "CLIENT 2 (RECEIVER)")

        self.log(self.client1_box, "Ready.")
        self.log(self.server_box, "Waiting for server...")
        self.log(self.client2_box, "Idle.")

    # =====================
    # UI HELPERS
    # =====================
    def make_panel(self, parent, title):
        frame = tk.Frame(parent, bg=BG, padx=10)
        frame.pack(side=tk.LEFT)

        tk.Label(
            frame,
            text=title,
            bg=BG, fg=FG,
            font=("Consolas", 11, "bold")
        ).pack()

        txt = tk.Text(
            frame,
            height=22,
            width=40,
            bg=BG, fg=FG,
            font=FONT,
            insertbackground=FG,
            relief=tk.FLAT
        )
        txt.pack()
        return txt

    def log(self, box, text):
        box.insert(tk.END, text + "\n")
        box.see(tk.END)

    def clear_all(self):
        self.client1_box.delete(1.0, tk.END)
        self.server_box.delete(1.0, tk.END)
        self.client2_box.delete(1.0, tk.END)

    # =====================
    # MAIN LOGIC
    # =====================
    def run_simulation(self):
        text = safe_text(self.entry.get())
        method = self.method_box.get()

        if not text or not method:
            return

        self.clear_all()

        # ===== CLIENT 1 =====
        control = compute_control(method, text)
        packet = f"{text}|{method}|{control}"

        self.log(self.client1_box, f"Data    : {text}")
        self.log(self.client1_box, f"Method  : {method}")
        self.log(self.client1_box, f"Control : {control}")
        self.log(self.client1_box, "Sending to server...")

        sender = socket.socket()
        sender.connect((HOST, PORT_SERVER))
        sender.send(packet.encode())
        sender.close()

        # ===== CLIENT 2 LISTENER =====
        receiver = socket.socket()
        receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiver.bind((HOST, PORT_CLIENT2))
        receiver.listen(1)

        conn, _ = receiver.accept()
        data = conn.recv(4096).decode()
        conn.close()
        receiver.close()

        # IMPORTANT: limited split
        recv_data, recv_method, recv_ctrl, _ = data.split("|", 3)

        # ===== SERVER PANEL =====
        self.log(self.server_box, f"Method        : {recv_method}")
        self.log(self.server_box, f"Original Data : {text}")
        self.log(self.server_box, f"Corrupted Data: {recv_data}")

        # ===== CLIENT 2 =====
        comp_ctrl = compute_control(recv_method, recv_data)

        self.log(self.client2_box, f"Received Data : {recv_data}")
        self.log(self.client2_box, f"Method        : {recv_method}")
        self.log(self.client2_box, f"Sent Ctrl     : {recv_ctrl}")
        self.log(self.client2_box, f"Computed Ctrl : {comp_ctrl}")

        if recv_ctrl == comp_ctrl:
            self.log(self.client2_box, "Status        : DATA CORRECT")
        else:
            self.log(self.client2_box, "Status        : DATA CORRUPTED")

        self.log(self.client2_box, f"Note          : {METHOD_INFO[recv_method]}")


if __name__ == "__main__":
    root = tk.Tk()
    DataComGUI(root)
    root.mainloop()
