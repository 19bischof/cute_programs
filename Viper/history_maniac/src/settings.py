import json
with open("secret.json") as f:
    obj = json.load(f)
user = obj['user']
passwd = obj['passwd']
ip = obj['ip']
file_name = 'data/current_history.txt'
file_path = '/history/current_history.txt'

