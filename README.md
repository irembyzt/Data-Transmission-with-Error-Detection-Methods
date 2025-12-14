# Data-Transmission-with-Error-Detection-Methods

Project Overview

This project demonstrates **data transmission with error detection techniques** using **socket programming**.  
The system simulates a real network by including:

- Random **error detection method selection**
- Random **error injection**
- Correct handling of **corrupted and non-corrupted data**

The project consists of **three main components**:

1. **Client 1 (Sender)**
2. **Server (Intermediate Node + Error Injector)**
3. **Client 2 (Receiver + Error Controller)**

---

Project Structure

```
project/
├── client1.py
├── client2.py
├── server.py
├── controls.py
├── errors.py
├── utils.py
├── main.py
└── README.md
```

---

Control Information Generation Methods

The system randomly selects **one of the following methods** for each transmission:

| Method | Description |
|------|------------|
| PARITY | Even parity based on total number of 1s |
| 2DPARITY | Row & column parity using matrix representation |
| CRC16 | Cyclic Redundancy Check |
| HAMMING | Hamming (7,4) code |
| CHECKSUM | Internet (IP) checksum |

---

Error Injection Methods

The server randomly applies one of the following error types or forwards the data without error:

- No Error
- Bit Flip
- Character Substitution
- Character Deletion
- Random Insertion
- Character Swap
- Multiple Bit Flips
- Burst Error

---

Packet Format

```
DATA | METHOD | CONTROL_INFORMATION | ERROR_FLAG
```

---

How to Run

Run in separate terminals:

```bash
python client2_receiver.py
python server_corruptor.py
python client1_sender.py

Conclusion
This project demonstrates realistic data transmission, error detection limitations, and modular socket-based design.
