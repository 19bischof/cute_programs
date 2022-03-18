from scratcher import imagine
import json
import requests
import os
import shutil

json_path = imagine.json_path
filter_path = imagine.filter_path
image_path = imagine.image_path

def save_full_from_filter():
    with open(json_path, "r") as f:
        dick = json.load(f)
    for name in os.listdir(filter_path):
        if name in os.listdir(image_path):  #already stored!
            continue
        if name not in dick.keys(): # copy file instead if there is no full version
            shutil.copyfile(filter_path+name,image_path+name)
            continue
        resp = requests.get(dick[name], stream=True)    # get the image from url
        imagine.write_image_from_resp(None,image_path+name, resp) 

if __name__ == "__main__":
    save_full_from_filter()