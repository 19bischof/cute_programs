# api call for website quotes.net
# Haven't received tokenid and uid yet
import requests


class quotes_dot_net_api_call:
    uid = ''
    tokenid = ''
    searchtype = ['RANDOM', 'SEARCH', 'AUTHOR']
    searchtype_index = 0
    search_query = ''
    format = 'json'
    url = 'https://www.stands4.com/services/v2/quotes.php?uid={0}&tokenid={1}&searchtype={2}&query={3}&format={4}'.format(
        uid, tokenid, searchtype[searchtype_index], search_query, format)

    def get():
        response = requests.get(quotes_dot_net_api_call.url+'?')
        json_quote = response.json()
        print(json_quote)
        return json_quote['results']['result']
