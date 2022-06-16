import requests
import random
import string
import json
from i_menu import i_menu
import webbrowser
import pickle


def get_query():
    max_page_number = 50
    number_of_options = 5
    page_number = random.randrange(1, max_page_number)
    printable = set(string.printable)
    print("page number", page_number)
    url = 'https://api.github.com/search/repositories'
    query = {'q': 'Python', 'per_page': number_of_options, 'page': page_number}
    header = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(url=url, headers=header, params=query)
    filtered = ''.join(filter(lambda x: x in printable, response.text))
    res = json.loads(filtered)
    options,urls,descriptions = [],[],[]
    for i in res['items']:
        options.append(i['full_name'])
        descriptions.append(i['description'])
        urls.append(i['html_url'])
    return {"options": options, "descriptions": descriptions,"urls":urls}


choice = i_menu(first_page=get_query(),callback_page=get_query).loop()
webbrowser.open(choice)
