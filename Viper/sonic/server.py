import socket
import time
import config as cg


with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,cg.buffer_size)
    sock.bind(cg.server_address)
    sock.recv(1024) #client sends speedtest request
    print("sending...")
    data = bytes([0xFF for _ in range(cg.chunk_size)]) # 1024 bytes
    start_t = time.perf_counter()
    while time.perf_counter() - start_t < cg.duration:
        sock.sendto(data,cg.client_address)