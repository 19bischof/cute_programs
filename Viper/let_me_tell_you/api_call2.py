# api call for website https://github.com/lukePeavey/quotable
import requests
from pprint import pprint

class quotable_dot_io_api_call:
    id = ''  # get quote by id like /quotes/:{id}
    tags = ''  # tags like '/quotes?=love|happiness'
    if id != '':
        tags = ''
    url = 'https://quotable.io/random'+id+tags

    def get():
        try:
            response = requests.get(quotable_dot_io_api_call.url)
        except:
            return None
        if (response.status_code == 200):
            json_quote = response.json()
            return {'content': json_quote['content'],'author' : json_quote['author'], 'tags' : json_quote['tags']}
        return None

if __name__ == "__main__":
    call = quotable_dot_io_api_call.get()
    pprint(call)