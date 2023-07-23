import json
with open("secret.json") as f:
    obj = json.load(f)
user = obj['user']
passwd = obj['passwd']
file_name = 'current_history.txt'
file_path = '/history/'+file_name
