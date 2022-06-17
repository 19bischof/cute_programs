# api call for website quotes.net
# Haven't received tokenid and uid yet
import requests


class quotes_dot_net_api_call:
    uid = '9472'
    token = 'uiGrwWzTtMe94oA3'
    searchtype = ['RANDOM', 'SEARCH', 'AUTHOR']
    searchtype_index = 0
    search_query = ''
    format = 'json'
    url = 'https://www.stands4.com/services/v2/quotes.php?uid={0}&tokenid={1}&searchtype={2}&query={3}&format={4}'.format(
        uid, token, searchtype[searchtype_index], search_query, format)

    def get():
        response = requests.get(quotes_dot_net_api_call.url,timeout=1)
        if (response.status_code == 200):
            json_quote = response.json()
            return {"content":json_quote['result']['quote'],"author":json_quote['result']['author']}
        return None