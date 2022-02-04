#this script shows the advantages of sets and lists
#____________________________________________________

# what i have learned with this script: 
# sets are way way way faster for membership checks especially in large lists (hashtable)
# lists are a lot faster when iterated through all members

import time
import string
import random
from tqdm import tqdm

def gen_string_ar(length):
    ar = []
    for i in range(length):
        k = random.randrange(4,8)
        ar.append(''.join(random.choices(string.ascii_lowercase, k=k)))
    return ar


def bench_membership(i,members,iter):
    start_t = time.perf_counter()
    hit = 0
    for l in tqdm(range(i)):
        if members[l] in iter:
            hit += 1
    print("hits:",hit)
    return time.perf_counter() - start_t

def bench_iteration(count,iter):
    start_t = time.perf_counter()
    for i in tqdm(range(count)):
        a_list = []
        for i in iter:
            a_list.append(i)
    return time.perf_counter()-start_t


def print_result(ar_t,buck_t):
    if ar_t > buck_t:
        print("The set was faster by {}%".format(format(100*ar_t/buck_t,".2f")))
    else:
        print("The list was faster by {}%".format(format(100*buck_t/ar_t,".2f")))


ar = gen_string_ar(1000 * 1000)
print("generated strings")
buck = set(ar)
print("initialized iterables")

print("starting membership benchmark")
count = 100
members = gen_string_ar(count)  #members are generated before benchmark so result is more pure
ar_t = bench_membership(count,members,ar)
buck_t = bench_membership(count,members,buck)
print_result(ar_t,buck_t)

print("starting iteration benchmark")
count = 100
ar_t = bench_iteration(count,ar)
buck_t = bench_iteration(count,buck)
print_result(ar_t,buck_t)