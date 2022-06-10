"""logic riddle from https://www.popularmechanics.com/science/math/a31153757/riddles-brain-teasers-logic-puzzles/
Three movie stars, Chloe, Lexa, and Jon, are filming a movie in the Amazon. They're very famous and very high-maintenance,
so their agents are always with them. One day, after filming a scene deep in the rainforest, the three actors and their agents
decide to head back to home base by foot. Suddenly, they come to a large river. On the riverbank, they find a small rowboat,
but it's only big enough to hold two of them at one time. The catch? None of the agents are comfortable leaving their movie star
with any other agents if they're not there as well. They don't trust that the other agents won't try to poach their star.
For example, Chloe's agent is okay if Chloe and Lexa are alone in the boat or on one of the riverbanks, but definitely not okay
if Lexa's agent is also with them. So how can they all get across the river?

"""

init_agents = [-1,-2,-3]
init_stars = [1,2,3]
# The Agent of 1 is -1
init_pool = [1,2,3,-1,-2,-3]
init_left_side = init_pool.copy()
init_right_side = []
next_side = {0:1,1:0} #0 is left, 1 is right

red = "\033[31m"
white = "\033[37m"
blue = "\033[34m"


def order_arr(a):
    pos,neg = [],[]
    for c in a:
        if c > 0:
            pos += [c]
        else:
            neg += [c]
    pos = sorted(pos)
    neg = sorted(neg)
    neg.reverse()
    return neg+pos


assert order_arr([2,-1,-3,3,-2,1]) == [-1,-2,-3,1,2,3]


def add_to_arr(s, c):
    s = s.copy()
    assert len(c) in (1, 2)
    s += c
    return s

def remove_from_arr(s, c):
    s = s.copy()
    assert len(s) >= len(c)
    for one_c in c:
        s.remove(one_c)
    return s
    


def find_permutations_from_pool(pool):
    lop = [[p] for p in pool]
    for ind, x in enumerate(pool):
        for y in pool[ind+1:]:
            lop.append([x,y])
    return lop


assert add_to_arr([-1,-2,-3], [1]) == [-1, -2, -3, 1]
assert add_to_arr([-1,2], [-2,3]) == [-1,2,-2,3]
assert add_to_arr([], [-1,3]) == [-1,3]
assert remove_from_arr([1,2,3], [1]) == [2,3]
assert remove_from_arr([-1,-2,2,3], [-1,3]) == [-2,2]
assert remove_from_arr([-2], [-2]) == []
assert find_permutations_from_pool([-1,-3,2]) == [[-1],[-3],[2],[-1,-3],[-1,2],[-3,2]]


def agent_alone_on_side(left, right):
    """True if not allowed"""
    for c in init_pool:
        assert c in left + right
    assert len(left) + len(right) == 6
    
    for side in (left, right):
        for star in init_stars:
            if star in side and star*-1 not in side:
                for agent in init_agents:
                    if agent in side:
                        return True
    return False


assert agent_alone_on_side([-1,-2,1], [-3,2,3]) == True
assert agent_alone_on_side([-1,-2,-3], [1,2,3]) == False
assert agent_alone_on_side([-3,-2,-1,1,2], [3]) == False
assert agent_alone_on_side([-1,-2,1,2,3], [-3]) == True


def agent_alone_on_boat(permut):
    """True if not allowed"""
    if len(permut) == 1:
        assert permut[0] in init_pool
        return False
    assert len(permut) == 2
    assert permut[0] != permut[1]

    for star in init_stars:
        if star in permut:
            for agent in init_agents:
                if agent in permut and agent*-1 != star:
                    return True
    return False


assert agent_alone_on_boat([-1,-2]) == False
assert agent_alone_on_boat([1]) == False
assert agent_alone_on_boat([1,-2]) == True
assert agent_alone_on_boat([1,2]) == False


def done(left, right):
    """True if done"""
    for c in init_pool:
        assert c in left + right
    assert len(left) + len(right) == 6
    return len(right) == 6


assert done([], [1,-2,3,-3,2,-1]) == True
assert done([-3], [2,-2,1,-1,3]) == False


def print_state(left, right, last, depth):
    for side in (order_arr(left), ":", order_arr(right)):
        for c in side:
            print(blue if c == last else "",c, end=white,sep="")
    print(red, depth, white)


def next_move(left_side, right_side, side, last, depth, depth_limit=100, out=True):
    if depth == depth_limit:  # set limit to prevent endless loop and go through all permutations before depth 100
        return
    assert side in next_side.keys()
    assert len(last) in (1, 2)
    for c in last:
        assert c in left_side + right_side
    assert len(left_side) + len(right_side) == 6
    for c in init_pool:
        assert c in left_side+right_side

    if out:
        print_state(left_side, right_side, last, depth)
    if done(left_side, right_side):
        return True

    agent_alone_on_side(left_side, right_side)

    if side == 0:
        current = left_side
    else:
        current = right_side
    permut_pool = find_permutations_from_pool(current)
    permut_pool.remove(last)
    for perm in permut_pool:
        if agent_alone_on_boat(perm):
            continue
        if side == 0:
            new_left = remove_from_arr(left_side, perm)
            new_right = add_to_arr(right_side, perm)
        else:
            new_left = add_to_arr(left_side, perm)
            new_right = remove_from_arr(right_side, perm)

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
        if not next_move(init_left_side, init_right_side, 0,[1], depth=0,
                         depth_limit=i, out=False):
            result = "un"
        print(result+"able to find the way with depth", i)
    print(f"Time taken: {time.perf_counter()-start_t:.2f} s")
# result is that at depth_limit 12 there is the first result
# -> 11 Moves are needed because in last depth there wasn't a move and
# at depth limit 12 there are depths 0 to 11 => 12 depths minus last one = 11
