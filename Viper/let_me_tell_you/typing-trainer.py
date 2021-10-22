import msvcrt
import sys
import os
from api_call2 import quotable_dot_io_api_call_ as q_io

red = '\033[91m'
white = '\033[37m'


def get_new_quote():
    return q_io.get()


# def print_task(pointer, the_quote):
    # if pointer < len(the_quote):
    #     # -1 so that space sets the input back and not the character before space but that may lead to index errors we'll see
    #     if the_quote[pointer -1] == ' ' or pointer == 0:
    #         os.system('cls' if os.name == 'nt' else 'clear')
    #         for i in range(len(the_quote)):

    #             if i < pointer:
    #                 prefix = red
    #             else:
    #                 prefix = white
    #             print(prefix + the_quote[i]+white, end="", flush=True)
    #         print()
    # else:
    #     os.system('cls' if os.name == 'nt' else 'clear')
    #     for i in range(len(the_quote)):

    #         if i < pointer:
    #             prefix = red
    #         else:
    #             prefix = white
    #         print(prefix + the_quote[i]+white, end="", flush=True)
    #     print()
    


def start_game():
    # this quote is from me
    
    the_quote = 'Today, as always, is not yesterday. So why does it feel like nothing has changed?'
    the_quote_data = get_new_quote()
    the_quote = the_quote_data['content']
    pointer = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    print(the_quote + '\r',end="")

    while pointer < len(the_quote):
        # print(pointer)
        # print("")
        sys.stdin.flush()

        # print("in the loop")
        key = msvcrt.getch()
        if key == bytes(the_quote[pointer], 'utf-8'):
            # print("increment")
            print(red+the_quote[pointer]+white, end="", flush=True)

            pointer += 1
        if key == b'\x03':
            quit()
        # print_task(pointer, the_quote)
    print()
    print('Quote by: {author}'.format(author=the_quote_data['author']))


while 1:
    start_game()
    if input("\nquit? ").lower() in ('quit', 'yes', 'y'):
        break

print("Thanks for playing!")
