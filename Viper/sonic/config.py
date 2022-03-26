chunk_size = 1024 * 8
duration = 10
timeout = 1
import json
with open("address.json","r") as f: #implement address.json locally
    dick = json.load(f)
server_address = (dick["server_address"],dick["server_port"])
client_address = (dick["client_address"],dick["client_port"])