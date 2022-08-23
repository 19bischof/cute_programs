#! usr/bin/python3.10
import random
import time
import re
from bs4 import BeautifulSoup
import requests
import mimetypes
import os
import json
import pathlib
project_path = pathlib.Path(__file__).absolute().parent.as_posix()
# url = "https://ipchicken.com/"
# resp = requests.get(url)

# soup = BeautifulSoup(resp.text, 'html.parser')
# # print(soup.select("body > table:nth-child(2) > tr:nth-child(1) > td:nth-child(3) > table:nth-child(5) > tr:nth-child(1) > td:nth-child(2) > font:nth-child(1)")
# #       [0].get_text().split('\n')[2])


class imagine:
    """parent class for dealing with images"""

    image_path = project_path+"/images/"
    filter_path = project_path+"filter/"
    json_path = filter_path+"000.json"

    def __init__(self):
        if not os.path.exists(self.filter_path):
            os.mkdir(self.filter_path)
        self.full_path_json = {}
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as f:
                self.full_path_json = json.load(f)

    def preview_to_filter(self, small_url, name, full_url):
        """save image_url to folder"""
        if self.is_duplicate(name):
            return
        resp = requests.get(small_url, stream=True)
        ext = mimetypes.guess_extension(resp.headers['Content-Type'])

        self.write_image_from_resp(self.filter_path+name+ext, resp)
        self.full_path_json[name+ext] = full_url
        with open(self.json_path, "w") as f:
            json.dump(self.full_path_json,f)

    def write_image_from_resp(self, path, resp):
        with open(path, 'wb') as f:
            if not resp.ok:
                print(resp)
                return
            for chunk in resp.iter_content(1024):  # writing with stream
                f.write(chunk)

    def is_duplicate(self, name):
        for file_path in (self.filter_path,self.image_path):
            files = os.listdir(file_path)
            for file in files:
                if file.startswith(name):
                    print("image already stored!")
                    return True
        return False


class scratcher:
    """parent class for scratching"""

    def __init__(self, url,delay = 0):
        self.browse(url,delay)

    def browse(self, url,delay):
        import urllib.request
        req = urllib.request.Request(url,headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:

            html = response.read().decode('utf-8')
        # time.sleep(delay)

        self.soup = BeautifulSoup(html, 'html.parser')  # the soup
        # print(self.soup.prettify())
        self.data = {}  # the extracted data

    def parse(self):
        """parse the soup"""
        pass

    def __repr__(self):
        string = ""
        for key, val in self.data.items():
            string += "{}: {}\n".format(key, val)
        return string


class chick(scratcher):
    """scratcher for ipchicken.com"""
    url = "https://www.ipchicken.com"

    def __init__(self):
        super().__init__(self.url)
        self.parse()

    def parse(self):
        pre = self.soup.select("body table td p font b")
        self.data['ipadress'] = pre[0].get_text().split('\n')[1]
        pre = self.soup.select("body table tr td table  tr td font")
        for key, val, slice in zip(("Name Address", "Port", "Browser"), pre, (14, 13, 9)):
            self.data[key] = val.get_text()[slice:]


class chain(scratcher):
    url = "https://www.blockchain.com/explorer/prices"

    def __init__(self):
        super().__init__(self.url,5)
        self.parse()
    def parse(self):
        # elem = self.soup.select_one("span.iQXny") #short-term method
        elem = self.soup.find("a",href='/explorer/assets/BTC')
        # print(elem.div.attrs['class'])
        # print(elem.div.div.attrs['class'])
        the_elem = elem.div.div.findNextSibling()
        self.data['Bitcoin in US'] = the_elem.get_text()
        
class unsplash(scratcher, imagine):
    """scratcher for unslpash.com"""
    # The soup select syntax was chosen on march 9nth for /backgrounds/nature
    # TODO: look at the following link yo https://unsplash.com/napi/landing_pages/backgrounds/desktop?page=2&per_page=20
    # its crazy they just give you the data in json format so yeah you can definetely improve the scraping process and simplify iter
    # do that tomorrow good day :) love you
    url = "https://unsplash.com/wallpapers/colors"

    def __init__(self):
        super().__init__(self.url)
        imagine.__init__(self)
        self.parse()

    def parse(self):
        self.data['alt'] = []
        self.data['highest'] = []
        self.data['thumb'] = []
        pre = self.soup.select(
            "div#app div div div.rJ2xz.bYpwS.U8eXG.M5vdR div div.mItv1 div.ripi6 figure div.YdIix div.L34o8 div.MbNnd div.zmDAx a.rEAWd div.omfF5 div.MorZF div.VQW0y.Jl9NH img.YVj9w")
        for  e in (pre):
            if hasattr(e, "alt"):
                try:  # maybe dont do this blindly and check first
                    self.data["alt"].append(e["alt"])
                    result = re.findall("[0-9]+w", e['srcset'])
                    int_result = [int(e[:-1]) for e in result]
                    # finding the highest qulality possible
                    highest = max(int_result)
                    thumb = [n for n in int_result if n > 300][0]
                    first_match = re.search(
                        str(highest) + "w", e["srcset"]).start()  # get end pos
                    second_match = re.search(result[int_result.index(
                        highest)-1], e["srcset"]).end()  # get start pos
                    self.data['highest'].append(
                        e['srcset'][second_match + 2:first_match - 1])

                    ## repeat

                    first_match = re.search(
                        str(thumb) + "w", e["srcset"]).start()  # get end pos
                    second_match = re.search(result[int_result.index(
                        thumb)-1], e["srcset"]).end()  # get start pos
                    self.data['thumb'].append(
                        e['srcset'][second_match + 2:first_match - 1])
                except KeyError or ValueError:
                    pass
        # chos_i = random.randrange(len(self.data['highest']))
        # print("chosen:", self.data['alt'][chos_i])
        for chos_i in range(len(self.data['highest'])):
            self.preview_to_filter(self.data['thumb'][chos_i], self.data['alt'][chos_i],self.data['highest'][chos_i])


class napi_unsplash(scratcher, imagine):
    url = "https://unsplash.com/napi/landing_pages/wallpapers?page={page}&per_page={per_page}"

    def __init__(self,page=1):
        self.page, self.per_page = page, 30
        scratcher.__init__(self,self.url)
        imagine.__init__(self)
        self.browse()
        self.parse()

    def browse(self,trash=90):
        self.json_resp = requests.get(self.url.format(
            **{"page": self.page, "per_page": self.per_page})).json()

    def parse(self):
        photos = self.json_resp['photos']
        for i in range(self.per_page):
            try:
                name = photos[i]['id']
                if photos[i]['alt_description']:
                    name = photos[i]['alt_description']
                print(name)
                self.preview_to_filter(photos[i]['urls']['small'],name,photos[i]['urls']['full'])
            except Exception as e:
                print(photos[i])
                raise e


if __name__ == "__main__":
    print(chick())
    import time
    # unsplash()
    # napi_unsplash(3)
    # for i in range(20):
    #     napi_unsplash()
    #     time.sleep(5)
    print(chain())
    # print(un)
    # url = 'https://images.unsplash.com/photo-1539200831626-cad7f58c765f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8MTl8fHxlbnwwfHx8fA%3D%3D&auto=format&fit=crop&w=2592&q=60'
    # imagine.save(None,url,"hey")

    #things do work right now nice :)