"""logic riddle from https://www.popularmechanics.com/science/math/a31153757/riddles-brain-teasers-logic-puzzles/
Three movie stars, Chloe, Lexa, and Jon, are filming a movie in the Amazon. They're very famous and very high-maintenance,
so their agents are always with them. One day, after filming a scene deep in the rainforest, the three actors and their agents
decide to head back to home base by foot. Suddenly, they come to a large river. On the riverbank, they find a small rowboat,
but it's only big enough to hold two of them at one time. The catch? None of the agents are comfortable leaving their movie star
with any other agents if they're not there as well. They don't trust that the other agents won't try to poach their star.
For example, Chloe's agent is okay if Chloe and Lexa are alone in the boat or on one of the riverbanks, but definitely not okay
if Lexa's agent is also with them. So how can they all get across the river?

agents = 'abc'
stars = 'ABC'
The Agent of 'B' is 'b'
"""

init_pool = "abcABC"
init_left_side = "abcABC"
init_right_side = ""
next_side = {"left": "right", "right": "left"}

red = "\033[31m"
white = "\033[37m"
blue = "\033[34m"


def order_str(s):
    up, low = "", ""
    for c in s:
        if c.upper() == c:
            up += c
        else:
            low += c
    up = sorted(up)
    low = sorted(low)
    return ''.join(low)+''.join(up)


assert order_str("BAcCba") == "abcABC"


def add_to_str(s, c):
    assert len(c) in (1, 2)
    return s + c


def remove_from_str(s, c):
    assert len(s) >= len(c)
    for one_c in c:
        s = s.replace(one_c, '')
    return s


def find_permutations_from_pool(pool):
    lop = [c for c in pool]
    for ind, x in enumerate(pool):
        for y in pool[ind+1:]:
            lop.append(x+y)
    return lop


assert add_to_str("abc", 'A') == "abcA"
assert add_to_str("aB", 'bC') == "aBbC"
assert add_to_str("", "aC") == "aC"
assert remove_from_str("ABC", "A") == "BC"
assert remove_from_str("abBC", "aC") == "bB"
assert remove_from_str("b", "b") == ""
assert find_permutations_from_pool("ace") == ["a", "c", "e", "ac", "ae", "ce"]


def agent_alone_on_side(left, right):
    """True if not allowed"""
    for c in init_pool:
        assert c in left + right
    assert len(left) + len(right) == 6
    stars = "ABC"

    for side in (left, right):
        for star in stars:
            if star in side and star.lower() not in side:
                for agent in stars.lower():
                    if agent in side:
                        return True
    return False


assert agent_alone_on_side("abA", "cBC") == True
assert agent_alone_on_side("abc", "ABC") == False
assert agent_alone_on_side("abcAB", "C") == False
assert agent_alone_on_side("abABC", "c") == True


def agent_alone_on_boat(permut):
    """True if not allowed"""
    if len(permut) == 1:
        assert permut in init_pool
        return False
    assert len(permut) == 2
    assert permut[0] != permut[1]

    stars = "ABC"
    for star in stars:
        if star in permut:
            for agent in stars.lower():
                if agent in permut and star.lower() != agent:
                    return True
    return False


assert agent_alone_on_boat("ab") == False
assert agent_alone_on_boat("A") == False
assert agent_alone_on_boat("Ab") == True
assert agent_alone_on_boat("AB") == False


def done(left, right):
    """True if done"""
    for c in init_pool:
        assert c in left + right
    assert len(left) + len(right) == 6
    return len(right) == 6


assert done("", "acBACb") == True
assert done("c", "abBAC") == False


def print_state(left, right, last, depth):
    for side in (order_str(left), ":", order_str(right)):
        for c in side:
            print(blue if c == last else ""+c, end=white)
    print(red, depth, white)


def next_move(left_side, right_side, side, last, depth, depth_limit=100, out=True):
    if depth == depth_limit:  # set limit to prevent endless loop and go through all permutations before depth 100
        return
    assert side in ("left", "right")
    assert len(last) in (1, 2)
    for c in last:
        assert c in left_side + right_side
    assert len(left_side) + len(right_side) == 6
    for c in "abcABC":
        assert c in left_side+right_side

    if out:
        print_state(left_side, right_side, last, depth)
    if done(left_side, right_side):
        return True

    agent_alone_on_side(left_side, right_side)

    if side == "left":
        current = left_side
    else:
        current = right_side
    permut_pool = find_permutations_from_pool(current)
    permut_pool.remove(last)
    for perm in permut_pool:
        if agent_alone_on_boat(perm):
            continue
        if side == "left":
            new_left = remove_from_str(left_side, perm)
            new_right = add_to_str(right_side, perm)
        else:
            new_left = add_to_str(left_side, perm)
            new_right = remove_from_str(right_side, perm)

        if agent_alone_on_side(new_left, new_right):
            continue
        if next_move(new_left, new_right, next_side[side], perm, depth+1, depth_limit=depth_limit, out=out):
            return True
        if out:
            print_state(left_side, right_side, last, depth)


if __name__ == "__main__":
    import time
    start_t = time.perf_counter()
    for i in range(100):
        result = ""
        if not next_move(init_left_side, init_right_side, "left", "a", depth=0,
                         depth_limit=i, out=False):
            result = "un"
        print(result+"able to find the way with depth", i)
    print(f"Time taken: {time.perf_counter()-start_t:.2f} s")
# result is that at depth_limit 12 there is the first result
# -> 11 Moves are needed because in last depth there wasn't a move and
# at depth limit 12 there are depths 0 to 11 => 12 depths minus last one = 11
