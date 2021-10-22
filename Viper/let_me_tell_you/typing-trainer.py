import msvcrt
import sys
import math
import os
import shutil
import random
import hashlib
import json
import time
from api_call2 import quotable_dot_io_api_call_ as q_io
from api_call import quotes_dot_net_api_call as q_net

red = '\033[91m'
turquoise = '\033[36m'
green = '\033[32m'  #TODO the linebreaker function doesnt work correctly at some cases
white = '\033[37m'
up = '\033[A'
down = '\033[B'

cutoff_points = []

def get_new_quote():
    
    os.system('cls' if os.name == 'nt' else 'clear')
    if (random.random() > 0):   
        quote_dict = q_io.get()    
        quote_dict = None
        print("quotable.io")
    else:
        print("quotes.net")
        quote_dict =  q_net.get()
    if (quote_dict == None):
        print("The used API is not available!\nLoading quote from storage...")
        time.sleep(0.5)
        with open('quotes.json','r') as file_r:
            file_json = json.loads(file_r.read())
            
            if (len(file_json)):
                # print(list(file_json.keys()),type(file_json.keys()))
                quote_dict = file_json[list(file_json.keys())[random.randint(0,len(file_json)-1)]]
            else:
                print("Couldn't find a quote. Exiting...")
                quit()
    else:
        hash_v = hashlib.sha256(quote_dict['content'].encode('utf-8')).hexdigest()[:16]
        with open('quotes.json','r') as file_r:
            file_json = json.loads(file_r.read())
            if (file_json.get(hash_v)== None):
                with open('quotes.json','w') as file_w:
                    file_json[hash_v] = quote_dict
                    json.dump(file_json,file_w)
    return quote_dict


def line_breaker(the_quote,width):
    shifted_by = 0
    for k in range(math.floor(len(the_quote)/width)):
        if (the_quote[(k+1)*width-1 - shifted_by] != ' '):
            for i in range(width):
                if (the_quote[(k+1)*width -i -2 -shifted_by] != ' '):
                    continue
                else:
                    cutoff_points.append((k+1)*width-i-2 - shifted_by)
                    shifted_by += i + 1
                    break

    print(width,cutoff_points)

def start_game():
    # this quote is from me
    # the_quote = 'Today, as always, is not yesterday. So why does it feel like nothing has changed?'
    the_quote_data = get_new_quote()
    the_quote = the_quote_data['content']
    pointer = 0
    width = shutil.get_terminal_size().columns
    line_breaker(the_quote,width)
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(len(the_quote)):
        if (i in cutoff_points):
            print(red + the_quote[i]+white+'\n',flush=True,end="")
        else:
            print(red+the_quote[i]+white,flush=True,end="")
    for i in range(math.floor(len(the_quote)/width)):
        print(up,end="",flush=True)
    print('\r',end="",flush=True)
        

    while pointer < len(the_quote):
        # print(pointer)
        # print("")
        sys.stdin.flush()

        # print("in the loop")
        key = msvcrt.getch()
        if key == bytes(the_quote[pointer], 'utf-8'):
            # print("increment")
            print(turquoise+the_quote[pointer]+white, end="", flush=True)
            if (pointer in cutoff_points):
                print(down + '\r',end="",flush=True)
            pointer += 1
        if key == b'\x03':
            os.system('cls' if os.name == 'nt' else 'clear')
            quit()

        # print_task(pointer, the_quote)
    print()
    print('Quote by: {author}'.format(author=the_quote_data['author']))


while 1:
    start_game()
    if input("\nquit? ").lower() in ('quit', 'yes', 'y'):
        break

print("Thanks for playing!")
