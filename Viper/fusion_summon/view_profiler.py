"""Show Function Profiles using snakeviz"""
import os
import subprocess
import time
import pathlib
pees = []
project_path = pathlib.Path(__file__).absolute().parent.as_posix()

path = project_path+"/profiler/"
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
