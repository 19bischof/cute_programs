"""module to guess passwords
-> implemented are pure numbers (without leading zero) and the other one is from a pool of possible characters"""
import datetime
import time
import os
import pathlib
project_path = pathlib.Path(__file__).absolute().parent.as_posix()
passw = input("Please put in your password!\n")
extended_pool = "0123456789abcdefghijklmnopqrstuvwxyz"
pool = "abcdefghijklmnopqrstuvwxyz"

def guess_from_dick(p):
    if not os.path.exists(project_path+"/fat_words.txt"):
        print("Dictionary not found in root!")
        return False
    with open(project_path+"/fat_words.txt","r") as f:
        words = f.read().splitlines()
        if p in words:
            return True

def guess_from_int(p):
    """Guesses numbers with no leading zeros"""
    cur_number = 1
    while cur_number != p:
        cur_number += 1
    return cur_number


def give_estimation_from_int():
    start_t = time.perf_counter()
    the_number = 555555  # 6digits
    guess_from_int(the_number)
    return (time.perf_counter() - start_t)/the_number


def guess_from_pool(p):
    """Guesses from pool of characters"""
    global pool
    #convert p to array of indexes of pool
    ar_p = [pool.index(c) for c in p]
    open(project_path+"/progress.txt", 'w') #reset file
    with open(project_path+"/progress.txt", 'a') as f:
        f.write(str(ar_p)+"\n")
        cur_index = [0]
        while cur_index != ar_p:
            # f.write(str(cur_index)+"\n")
            cur_index[-1] += 1
            i = 1
            if cur_index[-i] == len(pool):  # overflow is happening
                
                # make sure the start is uniform for each position
                cur_index[-i] -= 1
                try:
                    # if positions are overflowing
                    while cur_index[-i] == len(pool)-1:
                        cur_index[-i] = 0
                        i += 1
                    cur_index[-i] += 1                    
                except IndexError:  # all positions are overflowing -> new position
                    cur_index.append(0)
                    
    
    cur_guess = "".join([pool[i] for i in cur_index])
    return cur_guess


def give_estimation_from_pool():
    start_t = time.perf_counter()
    nop = 4  # number of positions
    guess_from_pool(pool[len(pool)//2] * nop)
    return (time.perf_counter() - start_t) / (len(pool) ** nop)

if __name__ == "__main__":
    found = False
    start_t = time.perf_counter()  
    try:
        new_passw = int(passw)
        if str(new_passw) != passw:
            raise ValueError
        passw = new_passw
        a_number = True
        print("-> Brute Force from Numbers")
    except ValueError:
        a_number = False
        print("-> guess from Dictionary")
        if guess_from_dick(passw):
            print("Found in Dictionary!")
            found = True
        else:
            print("-> Brute Force from pool")
            for c in passw:
                if c not in pool:
                    pool = extended_pool
                    print("-> extended_pool")
    if not found:
        if a_number:
            print(f"ETA: {(t_delta := give_estimation_from_int()* passw):.6f} seconds | {datetime.timedelta(seconds=t_delta)}")
            guess_from_int(passw)     #brute forcing
        else:
            print(f"ETA: {(t_delta := give_estimation_from_pool() * (len(pool)**len(passw))):.3f} seconds | {datetime.timedelta(seconds=t_delta)}")
            guess_from_pool(passw)    #brute forcing

    print(f"It took {(t_delta := time.perf_counter() - start_t) :.6f} seconds | {datetime.timedelta(seconds=t_delta)}")
