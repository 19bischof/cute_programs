from unicodedata import numeric
import requests
import random
import string
import json
from i_menu import i_menu
import webbrowser

max_page_number = 50
number_of_options = 5
printable = set(string.printable)
page_number = random.randrange(1, max_page_number)
print("page number", page_number)
url = 'https://api.github.com/search/repositories'
query = {'q': 'Python', 'per_page': number_of_options, 'page': page_number}
header = {'Accept': 'application/vnd.github.v3+json'}
response = requests.get(url=url, headers=header, params=query)
filtered = ''.join(filter(lambda x: x in printable, response.text))
res = json.loads(filtered)
options = []
descriptions = []
for i in res['items']:

    options.append(i['full_name'])
    descriptions.append(i['description'])
choice = i_menu(options, desc=descriptions, get_index=True)()
webbrowser.open(res['items'][choice]['html_url'])
