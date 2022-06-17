def gen_perm(pool,length,cur=[]):
    if len(cur) >= length:
        yield cur
        return True
    for n in pool:
        cur.append(n)
        yield from gen_perm(pool,length)
        cur.pop()
            
print(type(gen_perm))
for p in gen_perm((0,1),0):
    print(p)