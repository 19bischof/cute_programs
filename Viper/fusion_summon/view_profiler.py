import os
import subprocess
import time
pees = []
path = "./.profiler/"
for file in os.listdir(path):
    if not os.path.isfile(path+file):
        continue
    if not file.endswith(".profiler"):
        continue
    pees.append(subprocess.Popen(["snakeviz",path+file]))
    

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt or SystemExit:
    pass
finally:
    for p in pees:
        p.terminate()
