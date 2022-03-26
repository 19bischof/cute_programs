import logging
import socket
import time
import config as cg
import threading
logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(message)s")

tees = []

def send_dgrams(sock, client_address):
    data = bytes([0xFF for _ in range(cg.chunk_size)])
    start_t = time.perf_counter()
    while time.perf_counter() - start_t < cg.duration:
        sock.sendto(data,client_address)
    logging.info(f"finished sending to {client_address}...")


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(cg.server_address)
    sock.settimeout(cg.timeout)
    logging.info("initialized socket...")
    while True:
        try:
            data,client_address = sock.recvfrom(1024)
        except TimeoutError:
            continue
        logging.info(f"sending to {client_address}...")
        t = threading.Thread(target=send_dgrams,args=(sock,client_address))
        t.start()
        tees.append(t)
        