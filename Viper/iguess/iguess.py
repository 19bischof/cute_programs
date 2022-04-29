"""This Script guesses your random number from 1 to 100"""

class one_to_a_hundred:

    def __init__(self):
        self.pool = [x+1 for x in range(100)]

    def __call__(self):
        return self.guess_from_pool_1()

    
    def reset_pool(self):
        self.pool = [x+1 for x in range(100)]
        
    def guess_from_pool_0(self):
        import random
        print("Is your number {} ?".format(
            self.pool.pop(random.randrange(len(self.pool)))
            ))
        if input().lower() in ("yes","y"):
            return True

    def guess_from_pool_1(self):
        print("Is your number below {} ?".format(
            self.pool[cur_i:=len(self.pool)//2]
            )
        )
        if input().lower() in ("yes","y"):
            self.pool = self.pool[:cur_i]
        else:
            self.pool = self.pool[cur_i:]
        if len(self.pool) == 1:
            print(f"Your number is {self.pool[0]} !")
            return True
guess_n = one_to_a_hundred()
while not guess_n():
    pass

# sleep to let user see the result before exiting
import time
time.sleep(1)
