from copy import deepcopy
from itertools import chain

all_solutions = False
def pprint(a,pre=""):
    print(end=pre)
    for x in a:
        print(x)
    print()
solutions = {}
original = \
[[ 0, 3, 0,  0, 7, 8,  9, 1, 0 ],
  [ 0, 7, 0,  1, 9, 0,  3, 0, 8 ],
  [ 1, 9, 8,  3, 0, 0,  0, 0, 7 ],

  [ 8, 0, 9,  7, 2, 1,  0, 0, 0 ],
  [ 0, 0, 0,  8, 0, 0,  7, 9, 1 ],
  [ 7, 1, 3,  0, 0, 0,  8, 2, 0 ],

  [ 9, 0, 1,  0, 3, 7,  0, 8, 2 ],
  [ 0, 8, 7,  0, 1, 9,  0, 3, 0 ],
  [ 3, 0, 0,  0, 8, 0,  1, 7, 9 ]]

def check(sud:list):
    global solutions
    """
    return 0: wrong
    return 1: ok
    return 2: finished
    """
            
    for row in ([[i for i in row if i] for row in sud]):
        if len(set(row)) < len(row):
            return 0
    
    for col in [[i for i in col if i] for col in zip(*sud)]:
        if len(set(col)) < len(col):
            return 0
        
    boxes = [[] for x in range(9)]
    for i,row in enumerate(sud):
        for k,r in enumerate(row):
            if r:
                boxes[3*(i//3)+k//3].append(r)
                
    for box in boxes:
        if len(set(box)) < len(box):
            return 0
            
    for row in sud:
        if row.count(0):
            return 1
    solutions[tuple(chain(*sud))] = sud
    print("\rFound solution number",len(solutions)-1,end="")
    return 2

def recursive(sud:list,depth=0):
    match(check(sud)):
        case 0: return False
        case 2: return True
    # print(f"depth:{depth}")
    new = deepcopy(sud)
    if new[depth//9][depth%9]: 
        if recursive(new,depth+1) and not all_solutions: return True
    else:
        for s in (1,2,3,4,5,6,7,8,9):
            new[depth//9][depth%9] = s
            if recursive(new,depth+1) and not all_solutions: return True
            
if __name__ == "__main__":
    import time
    start_t = time.perf_counter()
    recursive(original)
    pprint(original,pre="original:\n")
    for i,s in enumerate(solutions.values()):
        pprint(s,pre=f"solution {i}:\n")
    print(f"number of unique solutions: {len(solutions)}")
    print(f"time taken: {time.perf_counter() - start_t:.4f} seconds")
    