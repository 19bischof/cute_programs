import json
chunk_size = 1024 * 8
duration = 10
timeout = 1

with open("address.json", "r") as f:  # implement address.json locally
    dick = json.load(f)
server_address = (dick["server_address"], dick["server_port"])
client_address = (dick["client_address"], dick["client_port"])

# local machine has to implement address.json
# like so
# {
#     "server_address": "192.168.n.n",
#     "server_port": 5556,
#     "client_address": "192.168.n.n",
#     "client_port" : 5557
# }