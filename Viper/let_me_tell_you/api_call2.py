# api call for website https://github.com/lukePeavey/quotable
import requests


class quotable_dot_io_api_call_:
    id = ''  # get quote by id like /quotes/:{id}
    tags = ''  # tags like '/quotes?=love|happiness'
    if id != '':
        tags = ''
    url = 'https://quotable.io/random'+id+tags

    def get():
        response = requests.get(quotable_dot_io_api_call_.url)
        if (response.status_code == 200):
            json_quote = response.json()
            return {'content': json_quote['content'],'author' : json_quote['author'], 'tags' : json_quote['tags']}
        return None