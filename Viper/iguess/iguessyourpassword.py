import time
passw = input("Please put in your password! (only numbers no leading 0)\n")


def guess_from_int(p):
    cur_number = 1
    while cur_number != p:
        cur_number += 1
    return cur_number

def give_estimation_from_int():
    start_t = time.perf_counter()
    the_number = 555555 #6digits
    guess_from_int(the_number)
    return (time.perf_counter() - start_t)/the_number

def guess_from_pool(p):
    open("progress.txt",'w')
    with open("progress.txt",'a') as f:
        pool = "abcdefghijklmnopqrstuvwxyz"
        cur_guess = "a"
        cur_index = [0]
        while cur_guess != p:
            f.write(cur_guess+"\n")
            cur_index[-1] += 1
            i = 1
            if cur_index[-i] == len(pool): #overflow is happening
    ##            
                cur_index[-i] -= 1      #make sure the start is uniform for each position
                try:
                    while cur_index[-i] == len(pool)-1: #if positions are overflowing
                        cur_index[-i] = 0
                        i += 1
                    cur_index[-i] += 1
                except IndexError: #all positions are overflowing -> new position
                    cur_index.append(0)
        ##                cur_guess[:-i]
        ##                print(cur_index[-1],pool)
        ##                pool[cur_index[-i]]
        ##                cur_guess[-i+1:]
                            
            cur_guess = "".join([pool[i] for i in cur_index])
    return cur_guess

def give_estimation_from_pool():
    start_t = time.perf_counter()
    nop = 3 #number of positions
    guess_from_pool("m" * nop) 
    return (time.perf_counter() - start_t) ** (1/26)
print(f"ETA: {give_estimation_from_pool() ** len(passw):.6f} seconds")
##print(f"ETA: {give_estimation_from_int()* passw:.6f} seconds")
print("guessing...")
start_t = time.perf_counter()
p_found = guess_from_pool(passw)
print(f"Your password is {p_found}")
print(f"It took {time.perf_counter() - start_t :.6f} seconds")
