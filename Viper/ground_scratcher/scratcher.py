from bs4 import BeautifulSoup
import requests

# url = "https://ipchicken.com/"
# resp = requests.get(url)

# soup = BeautifulSoup(resp.text, 'html.parser')
# # print(soup.select("body > table:nth-child(2) > tr:nth-child(1) > td:nth-child(3) > table:nth-child(5) > tr:nth-child(1) > td:nth-child(2) > font:nth-child(1)")
# #       [0].get_text().split('\n')[2])


class scratcher:
    """parent class of scratchers"""

    def __init__(self, url):
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
        pre[0]['alt']
        self.data['ipadress'] = pre[0].get_text().split('\n')[1]
        pre = self.soup.select("body table tr td table  tr td font")
        for key, val, slice in zip(("Name Address", "Port", "Browser"), pre, (14, 13, 9)):
            self.data[key] = val.get_text()[slice:]


class unsplash(scratcher):
    """scratcher for unslpash.com"""
    url = "https://unsplash.com/backgrounds/nature"

    def __init__(self):
        super().__init__(self.url)
        self.parse()

    def parse(self):
        self.data['alts'] = []
        self.data['links'] = []
        pre = self.soup.select("div#app div div div.rJ2xz.bYpwS.U8eXG.M5vdR div div.mItv1 div.ripi6 figure div.YdIix div.L34o8 div.MbNnd div.zmDAx a.rEAWd div.omfF5 div.MorZF div.VQW0y.Jl9NH img.YVj9w")
        for e in pre:
            if hasattr(e,"alt"):
                try:
                    self.data["alts"].append(e["alt"])
                    self.data["links"].append(e["src"])#srcset is the way to get the best quality images yo
                except KeyError:
                    pass
                


if __name__ == "__main__":
    # print(chick())
    un = unsplash()
    print(un)

