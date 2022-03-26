import logging
import socket
import time
import config as cg
from _thread import start_new_thread
logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(message)s")

tees = []

def send_dgrams( client_address):
    with socket.socket(type=socket.SOCK_DGRAM) as sock:
        data = bytes([0xFF for _ in range(cg.chunk_size)])
        start_t = time.perf_counter()
        while time.perf_counter() - start_t < cg.duration:
            try:
                sock.sendto(data,client_address)
            except ConnectionResetError:
                logging.error(f"Connection with {client_address} was closed")
                return
        logging.info(f"finished sending to {client_address}...")


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(cg.server_address)
    sock.settimeout(cg.timeout)
    logging.info(f"initialized socket on {cg.server_address}...")
    while True:
        try:
            data,client_address = sock.recvfrom(1024)
        except TimeoutError:
            continue
        logging.info(f"sending to {client_address}...")
        start_new_thread(target=send_dgrams,args=[client_address])

        