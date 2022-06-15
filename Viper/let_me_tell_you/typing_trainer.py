import sys, os, shutil
import math, random, hashlib
import json, time
import pathlib
from api_call2 import quotable_dot_io_api_call as q_io
from api_call import quotes_dot_net_api_call as q_net
from getch import Getch
from list_of_praises import lop
from list_of_insults import loi

if os.name == 'nt':
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW("Did I wake you? 💋")
else:
    sys.stdout.write('\33]0;' + "Did I wake you? 💋" + '\a')
    sys.stdout.flush()
red = "\033[91m"
turquoise = "\033[36m"
green = "\033[32m"
reset = "\033[0m"
up = "\033[A"
down = "\033[B"
json_file_path = pathlib.Path(__file__).parent.absolute().as_posix() + "/quotes.json"
fail_limit = 0

if sys.argv:
    for ind,arg in enumerate(sys.argv):
        if arg.strip() in ("-l","--limit","/l"):
            try:
                next_arg = sys.argv[ind+1]
                if next_arg.isdigit():
                    fail_limit = int(next_arg)
            except IndexError: pass
        elif arg.strip() in ("-h","--help","/h"):
            print("A typing trainer with famous quotes"+
            "\nUsage: python.exe *this-file* [(-l|--limit) number, (-h|--help)]")
            quit()


def get_new_quote():

    os.system("cls" if os.name == "nt" else "clear")
    if random.random() > 0:
        print("fetching from quotable.io...", flush=True)
        quote_dict = q_io.get()
    else:
        print("fetching from quotes.net...", flush=True)
        quote_dict = q_net.get()
    if quote_dict == None:

        print("The used API is not available!")
        time.sleep(0.5)
        print("Loading quote from storage...")
        time.sleep(1)
        with open(json_file_path, "r") as f:
            try:
                file_json = json.load(f)
            except json.JSONDecodeError:
                print("Couldn't load from storage!")
                quit()
            if len(file_json):
                quote_dict = file_json[
                    list(file_json.keys())[random.randint(0, len(file_json) - 1)]
                ]
            else:
                print("Couldn't find a quote. Exiting...")
                quit()

    return quote_dict


def line_breaker(the_quote, width, cutoff_points):
    # makes sure that at the EOL in the terminal there will always be a space, so that a word isn't cut off
    shifted_by = 0
    k = 0
    while k < (math.floor((len(the_quote) + shifted_by) / width)):
        # for each line of the quote in terminal
        if the_quote[(k + 1) * width - 1 - shifted_by] != " ":
            # if quote-character at EOL in terminal not a space -> search to the left for next space
            for i in range(1, width):
                # searching leftwards until a space is found
                if the_quote[(k + 1) * width - i - 1 - shifted_by] != " ":
                    continue
                else:
                    # found the space after searching leftwards from EOL

                    cutoff_points.append((k + 1) * width - i - 1 - shifted_by)
                    shifted_by += i  # quote length is now increased in terminal, because of artificial linebreak, so this keeps track of the increased size
                    break
        else:
            # found space at EOL
            cutoff_points.append((k + 1) * width - 1 - shifted_by)
        k += 1


# well now i know that what i wrote is completely obsolete since there is a very nice module called textwrap
# that does this exact same thing but I'm just gonna keep what I wrote, since it would feel like a waste (●'◡'●)


def save_quote(quote_dict):
    hash_v = hashlib.sha256(quote_dict["content"].encode("utf-8")).hexdigest()[:16]
    with open(json_file_path, "r") as f:
        try:
            file_json = json.load(f)
        except json.JSONDecodeError:
            file_json = {}
    with open(json_file_path,'w') as f:
        file_json[hash_v] = quote_dict
        json.dump(file_json, f,indent=4)
            


def start_game(cutoff_points):
    # this quote is from me
    # the_quote = 'Today, as always, is not yesterday. So why does it feel like nothing has changed?'

    the_quote_data = get_new_quote()
    the_quote = the_quote_data["content"]

    pointer = 0
    width = shutil.get_terminal_size().columns
    line_breaker(the_quote, width, cutoff_points)

    os.system("cls" if os.name == "nt" else "clear")
    for i in range(len(the_quote)):
        if i in cutoff_points:
            print(red + the_quote[i] + reset + "\n", flush=True, end="")
        else:
            print(red + the_quote[i] + reset, flush=True, end="")

    for i in range(len(cutoff_points)):
        print(up, end="", flush=True)
    print("\r", end="", flush=True)

    # user character input starts here:
    wrong_input = 0
    start_time = 0
    getch = Getch()  # instancing
    while pointer < len(the_quote):
        sys.stdin.flush()

        key = getch()
        if key == b"\x03":  # if CTRL + C
            os.system("cls" if os.name == "nt" else "clear")
            quit()
        if key == bytes(the_quote[pointer], "utf-8"):  # if correct chararcter input
            if not start_time:                          #starts time only when correct first character correct
                start_time = time.perf_counter()
            print(turquoise + the_quote[pointer] + reset, end="", flush=True)
            if pointer in cutoff_points:
                print(down + "\r", end="", flush=True)
            pointer += 1
        else:
            wrong_input += 1
            if wrong_input > fail_limit:
                insult = random.choice(loi)
                os.system("cls" if os.name == "nt" else "clear")
                print("Assessment:",insult)
                quit()
            

    print("\nQuote by: {author}".format(author=the_quote_data["author"]))
    # 5 characters are a word
    wpm = (len(the_quote)-1) / 5 / ((time.perf_counter() - start_time) / 60)
    print("wpm:", wpm.__format__(".2f"))
    print(
        "accuracy:",
        ((len(the_quote) / (len(the_quote) + wrong_input)) * 100).__format__(".2f")
        + "%",
    )
    praise = random.choice(lop)
    print("Comment: " + praise + ("" if praise.endswith("!") else "!"))
    save_quote(the_quote_data)


while 1:
    cutoff_points = []
    start_game(cutoff_points)
    try:
        if input("quit?\n").lower().strip() in ("quit", "q", "yes", "y", "exit"):
            break
    except KeyboardInterrupt:
        break
print("I'm a game and you're a player 💋!")
