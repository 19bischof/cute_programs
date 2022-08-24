def gen_perm(pool,length,cur=[]):
    """Each iteration of this call represents one index. The list "cur" is for all recursions up to date.
    The for loop goes through each possible element for this index.
    And then it calls gen_perm to generate all values for the next index. 
    Once a previous index gets a new value all following indeces need to generate all values again"""
    if len(cur) >= length:
        yield cur       #yields one permutation
        return True
    for n in pool:
        cur.append(n)           #next value of current digit
        yield from gen_perm(pool,length) #calls for following digits to be generated
        cur.pop()               #prepares for next value of current digit
            
for p in gen_perm((0,1),5):
    print(p)