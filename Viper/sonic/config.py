import json
import pathlib

chunk_size = 1024 * 8
duration = 10
timeout = 0.5
root_path = pathlib.Path(__file__).parent.as_posix()
with open(root_path + "/address.json", "r") as f:  # implement address.json locally
    dick = json.load(f)
server_address = (dick["server_address"], dick["server_port"])
client_address = (dick["client_address"], dick["client_port"])

# local machine has to implement address.json
# like so
# {
#     "server_address": "192.168.n.n",
#     "server_port": 44412,
#     "client_address": "192.168.n.n",
#     "client_port" : 44413
# }