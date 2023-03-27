# this script shows the advantages of sets and lists
# ____________________________________________________

# what i have learned with this script:
# sets are way way way faster for membership checks especially in large lists (hashtable)
# lists are a lot faster when iterated through all members

import time
import string
import random
from tqdm import tqdm


def gen_string_ar(length):
    "generates a random string length times"
    ar = []
    for i in range(length):
        k = random.randrange(4, 8)
        ar.append(''.join(random.choices(string.ascii_lowercase, k=k)))
    return ar


def bench_membership(count, members, iter, desc=""):
    """checking if iterable includes members"""
    start_t = time.perf_counter()
    hit = 0
    for l in tqdm(range(count), desc=desc):
        if members[l] in iter:
            hit += 1
    # print("hits:",hit)
    return time.perf_counter() - start_t


def bench_iteration(count, iter, desc=""):
    """iterating over the entire iterable"""
    start_t = time.perf_counter()
    for i in tqdm(range(count), desc=desc):
        a_list = []
        for i in iter:
            a_list.append(i)
    return time.perf_counter()-start_t


def print_result(ar_t, buck_t):
    if ar_t > buck_t:
        print("The Set was faster by {}%".format(
            format(100*ar_t/buck_t - 100, ".2f")))
    else:
        print("The List was faster by {}%".format(
            format(100*buck_t/ar_t - 100, ".2f")))
    print()


if __name__ == "__main__":
    print("\n")
    print("------------ initializing array and set ------------")
    
    ar = gen_string_ar(length := 1_000_000)
    buck = set(ar)
    print(f"initialized with {length} words")
    print("------------ starting membership benchmark ------------")
    count = 1000
    # members are generated before benchmark so result is more pure
    members = gen_string_ar(count)
    ar_t = bench_membership(count, members, ar, desc="List")
    buck_t = bench_membership(count, members, buck, desc="Set ")
    print_result(ar_t, buck_t)

    print("------------ starting iteration benchmark ------------")
    count = 100
    ar_t = bench_iteration(count, ar, desc="List")
    buck_t = bench_iteration(count, buck, desc="Set ")
    print_result(ar_t, buck_t)
