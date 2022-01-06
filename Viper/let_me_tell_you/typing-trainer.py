import msvcrt
import sys
import math
import os
import pathlib
import shutil
import random
import hashlib
import json
import time
import pathlib
from api_call2 import quotable_dot_io_api_call as q_io
from api_call import quotes_dot_net_api_call as q_net

red = '\033[91m'
turquoise = '\033[36m'
green = '\033[32m'  
white = '\033[37m'
up = '\033[A'
down = '\033[B'
json_file_path = pathlib.Path(
    __file__).parent.absolute().__str__() + '\quotes.json'


def get_new_quote():

    os.system('cls' if os.name == 'nt' else 'clear')
    if (random.random() > 0):
        print("fetching from quotable.io...", flush=True)
        quote_dict = q_io.get()
    else:
        print("fetching from quotes.net...", flush=True)
        quote_dict = q_net.get()
    if (quote_dict == None):

        print("The used API is not available!")
        time.sleep(0.5)
        print("Loading quote from storage...")
        time.sleep(1)
        with open(json_file_path, 'r') as file_r:
            file_json = json.loads(file_r.read())
            # input("number of quotes in local file:" + str(len(list(file_json.keys()))))  #lists the number of quotes in quotes.json
            if (len(file_json)):
                quote_dict = file_json[list(file_json.keys())[
                    random.randint(0, len(file_json)-1)]]
            else:
                print("Couldn't find a quote. Exiting...")
                quit()

    return quote_dict


def line_breaker(the_quote, width, cutoff_points):
    # makes sure that at the EOL in the terminal there will always be a space, so that a word isn't cut off
    shifted_by = 0
    k = 0
    while k < (math.floor((len(the_quote) + shifted_by)/width)):
    # for each line of the quote in terminal
        if (the_quote[(k+1)*width-1 - shifted_by] != ' '):
        # if quote-character at EOL in terminal not a space -> search to the left for next space
            for i in range(1, width):
                # searching leftwards until a space is found
                if (the_quote[(k+1)*width - i - 1 - shifted_by] != ' '):
                    continue
                else:
                    # found the space after searching leftwards from EOL

                    cutoff_points.append((k+1)*width-i-1 - shifted_by)
                    shifted_by += i  # quote length is now increased in terminal, because of artificial linebreak, so this keeps track of the increased size
                    break
        else:
            # found space at EOL
            cutoff_points.append((k+1)*width-1 - shifted_by)
        k += 1


def save_quote(quote_dict):
    hash_v = hashlib.sha256(
        quote_dict['content'].encode('utf-8')).hexdigest()[:16]
    with open(json_file_path, 'r') as file_r:
        file_json = json.loads(file_r.read())
        if (file_json.get(hash_v) == None):
            with open(json_file_path, 'w') as file_w:
                file_json[hash_v] = quote_dict
                json.dump(file_json, file_w)


def start_game(cutoff_points):
    # this quote is from me
    # the_quote = 'Today, as always, is not yesterday. So why does it feel like nothing has changed?'

    the_quote_data = get_new_quote()
    the_quote = the_quote_data['content']

    pointer = 0
    width = shutil.get_terminal_size().columns
    line_breaker(the_quote, width, cutoff_points)


    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(len(the_quote)):
        if (i in cutoff_points):
            print(red + the_quote[i]+white+'\n', flush=True, end="")
        else:
            print(red+the_quote[i]+white, flush=True, end="")

    for i in range(len(cutoff_points)):
        print(up, end="", flush=True)
    print('\r', end="", flush=True)

    # user character input starts here:
    start_time = time.time()
    while pointer < len(the_quote):
        sys.stdin.flush()

        key = msvcrt.getch()
        if key == bytes(the_quote[pointer], 'utf-8'):  # if correct chararcter input
            print(turquoise+the_quote[pointer]+white, end="", flush=True)
            if (pointer in cutoff_points):
                print(down + '\r', end="", flush=True)
            pointer += 1
        if key == b'\x03':  # if CTRL + C
            os.system('cls' if os.name == 'nt' else 'clear')
            quit()

    print()
    print('Quote by: {author}'.format(author=the_quote_data['author']))
    # 5 characters are a word
    wpm = len(the_quote) / 5 / ((time.time()-start_time) / 60)
    print("wpm:", wpm.__format__(".2f"))
    save_quote(the_quote_data)


while 1:
    cutoff_points = []
    start_game(cutoff_points)
    if input("\nquit? ").lower().strip() in ('quit', 'yes', 'y'):
        break

print("Thanks for playing!")
