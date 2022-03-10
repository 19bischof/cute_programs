import os
import subprocess
import time
pees = []
for file in os.listdir():
    if not os.path.isfile(file):
        continue
    if not file.endswith(".profiler"):
        continue
    pees.append(subprocess.Popen("snakeviz {}".format(file)))

time.sleep(1)
for p in pees:
    p.terminate()