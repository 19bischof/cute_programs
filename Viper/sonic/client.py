import time
import socket
import config as cg
cur_count = 0
all_count = 0
update_interval = 0.5
units = ("bps","Kbps","Mbps","Gbps","Tbps","Pbps")

#Currently work with 1024 as factor difference because of Windows preference

def calc_rate(rate):
    ind = 0
    rate *= 8  #show result in bits
    while rate > 1024 ** (ind+1):
        ind += 1
    if ind != 0:
        rate /= (1024 ** ind) 
    return units[ind],rate

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
    sock.bind(cg.client_address)
    sock.settimeout(cg.timeout)
    sock.sendto(b'I am wide open',cg.server_address)
    start_t = time.perf_counter()
    last_t = start_t
    while True:
        try:
            data = sock.recv(cg.chunk_size)
        except TimeoutError:
            end_t = time.perf_counter() - cg.timeout
            break
        cur_count += 1
        all_count += 1
        if time.perf_counter() - last_t > update_interval:
            rate = cur_count*cg.chunk_size/(time.perf_counter() - last_t)
            cur_unit,rate = calc_rate(rate)
            print(f"{rate:6.2f} {cur_unit}\r",end="")
            last_t = time.perf_counter()
            cur_count = 0

all_rate = all_count*cg.chunk_size/(end_t - start_t)
unit, rate = calc_rate(all_rate)
print(f"avg: {rate:6.2f} {unit}")