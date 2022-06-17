"""logic riddle from https://www.popularmechanics.com/science/math/a31153757/riddles-brain-teasers-logic-puzzles/
In some future time, when the shelter-in-place bans are lifted, a married couple, Florian and Julia,
head over to a bar to celebrate their newfound freedom.They find four other couples there who had the same idea.
Eager for social contact, every person in the five couples enthusiastically taps elbows (the new handshake) with 
each person they haven't yet met. It actually turns out many of the people had known each other prior, so when 
Julia asks everyone how many elbows they each tapped, she remarkably gets nine different answers!
The question: How many elbows did Florian tap? """

# solution: a dictionary that stores each answer(0-8) as keys(0-8) with a list of indexes that it bumped with as value

import time
num_of_people = 4
# all indeces of people go from 0 to 9
pool = list(range(0, num_of_people))  # original: range(0,10)


class curious_dick(dict):

    def set_new(self, key, value) -> None:
        print("setnew",key,value)
        assert type(value) == tuple
        assert key in range(0, num_of_people)
        assert key not in value
        if self.value_check(key, value):
            super().__setitem__(key, value)
            return True
        return False

    def value_check(self, key, value):
        count = 0
        try:
            for k, v in self.items():
                assert v != value
                if key == k:
                    continue
                if key in v:
                    count += 1
                    assert k in value  # all other answer bumps need to be in value
            # logic error: more people bumped person than his answer
            assert count <= len(value)
            _keys = self.keys()
            for v in value:
                if v in _keys:
                    # values are connected to others if exists
                    assert key in self[v]
        except AssertionError:
            return False
        return True


def assert_raises(d: curious_dick, key, value, error):
    cond = False
    d_before = d.copy()
    try:
        cond = not(d.set_new(key, value))

    except error:
        cond = True
    assert cond == True
    assert d_before == d


def test_curious():
    d = curious_dick()
    d.set_new(0, ())
    assert_raises(d, 1, 2, AssertionError)
    assert_raises(d, 1, (0,), AssertionError)
    assert_raises(d, 1, (1, 2), AssertionError)
    assert_raises(d, 1, (), AssertionError)
    d.set_new(1, (2, 3))
    assert_raises(d, 2, (3, 5), AssertionError)
    assert_raises(d, 2, (num_of_people-1,), AssertionError)


test_curious()


def gen_perm(pool, length, cur=[]):
    if len(cur) >= length:
        yield tuple(cur)
        return True
    for n in pool:
        cur.append(n)
        yield from gen_perm(pool, length,cur)
        cur.pop()


def gen_from_pool(not_this):
    my_pool = pool.copy()  # not this becomes None at end
    my_pool.remove(not_this)
    cur_length = 0
    new = []
    while (cur_length <= num_of_people - 2):
        yield from gen_perm(my_pool, cur_length,new)
        cur_length += 1


for p in gen_from_pool(3):
    print("yield:", p)
    # time.sleep(0.2)


def copy_dick(d: curious_dick):
    new = curious_dick()
    for key, value in d.items():
        new[key] = value
    return new


def path_finding(answers: curious_dick):
    if len(answers) >= num_of_people-1:
        return answers
    for person in pool:
        print("person",person)
        for value in gen_from_pool(person):
            if not answers.set_new(person, value):
                continue
            if value:=path_finding(copy_dick(answers)):
                return value



print(path_finding(the_dick := curious_dick()))
