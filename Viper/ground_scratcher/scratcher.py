#! usr/bin/python3.10
import random
import re
from bs4 import BeautifulSoup
import requests
import mimetypes
# url = "https://ipchicken.com/"
# resp = requests.get(url)

# soup = BeautifulSoup(resp.text, 'html.parser')
# # print(soup.select("body > table:nth-child(2) > tr:nth-child(1) > td:nth-child(3) > table:nth-child(5) > tr:nth-child(1) > td:nth-child(2) > font:nth-child(1)")
# #       [0].get_text().split('\n')[2])


class imagine:
    """parent class for dealing with images"""

    def save(self, url, name):
        """save image_url to folder"""
        resp = requests.get(url, stream=True)
        ext = mimetypes.guess_extension(resp.headers['Content-Type'])
        with open("images/"+name+ext, 'wb') as f:
            if not resp.ok:
                print(resp)
                return
            for chunk in resp.iter_content(1024): #writing with stream
                f.write(chunk)


class scratcher:
    """parent class for scratching"""

    def __init__(self, url):
        self.browse(url)
        
    def browse(self,url):
        self.soup = BeautifulSoup(
            requests.get(url).text, 'html.parser')  # the soup
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
    url = "https://ipchicken.com"

    def __init__(self):
        super().__init__(self.url)
        self.parse()

    def parse(self):
        pre = self.soup.select("body table td p font b")
        self.data['ipadress'] = pre[0].get_text().split('\n')[1]
        pre = self.soup.select("body table tr td table  tr td font")
        for key, val, slice in zip(("Name Address", "Port", "Browser"), pre, (14, 13, 9)):
            self.data[key] = val.get_text()[slice:]


class unsplash(scratcher, imagine):
    """scratcher for unslpash.com"""
    #The soup select syntax was chosen on march 9nth for /backgrounds/nature
    TODO: look at the following link yo https://unsplash.com/napi/landing_pages/backgrounds/desktop?page=2&per_page=20
    its crazy they just give you the data in json format so yeah you can definetely improve the scraping process and simplify iter
    do that tomorrow good day :) love you
    url = "https://unsplash.com/backgrounds/desktop"

    def __init__(self):
        super().__init__(self.url)  # left to right super() parent unless incest
        self.parse()

    def parse(self):
        self.data['alt'] = []
        self.data['highest'] = []
        pre = self.soup.select(
            "div#app div div div.rJ2xz.bYpwS.U8eXG.M5vdR div div.mItv1 div.ripi6 figure div.YdIix div.L34o8 div.MbNnd div.zmDAx a.rEAWd div.omfF5 div.MorZF div.VQW0y.Jl9NH img.YVj9w")
        for ind, e in enumerate(pre):
            if hasattr(e, "alt"):
                try:  # maybe dont do this blindly and check first
                    self.data["alt"].append(e["alt"])
                    result = re.findall("[0-9]+w", e['srcset'])
                    int_result = [int(e[:-1]) for e in result]
                    # finding the highest qulality possible
                    highest = max(int_result)
                    first_match = re.search(
                        str(highest) + "w", e["srcset"]).start()  # get end pos
                    second_match = re.search(result[int_result.index(
                        highest)-1], e["srcset"]).end()  # get start pos
                    self.data['highest'].append(
                        e['srcset'][second_match + 2:first_match - 1])
                except KeyError or ValueError:
                    pass
        chos_i = random.randrange(len(self.data['highest']))
        print("chosen:",self.data['alt'][chos_i])
        self.save(self.data['highest'][chos_i], self.data['alt'][chos_i])


if __name__ == "__main__":
    # print(chick())
    un = unsplash()
    # print(un)
    # url = 'https://images.unsplash.com/photo-1539200831626-cad7f58c765f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8MTl8fHxlbnwwfHx8fA%3D%3D&auto=format&fit=crop&w=2592&q=60'
    # imagine.save(None,url,"hey")
