import threading
import time
from client1 import client1
from client2 import client2
from server import server
from utils import safe_text

def main():
    text = safe_text(input("Text: "))

    t2 = threading.Thread(target=client2)
    ts = threading.Thread(target=server)

    t2.start()
    time.sleep(0.1)
    ts.start()
    time.sleep(0.1)

    client1(text)

if __name__ == "__main__":
    main()
