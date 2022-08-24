"""logic riddle from https://www.popularmechanics.com/science/math/a31153757/riddles-brain-teasers-logic-puzzles/
In some future time, when the shelter-in-place bans are lifted, a married couple, Florian and Julia,
head over to a bar to celebrate their newfound freedom.They find four other couples there who had the same idea.
Eager for social contact, every person in the five couples enthusiastically taps elbows (the new handshake) with 
each person they haven't yet met. It actually turns out many of the people had known each other prior, so when 
Julia asks everyone how many elbows they each tapped, she remarkably gets nine different answers!
The question: How many elbows did Florian tap? """

pool_of_answers = list(range(9)) # min 0 taps, max 8 taps
answer_list = [[] for x in range(9)] # index 0 is Florian, 1 and 2 are partners;3 and 4, 5 and 6, 7 and 8 are partners
#in each index is a list of indexes you bumped elbows with
#value -1 ist Julia

def valid_answer_list():
    previous_answers = []
    try:
        for index,person in enumerate(answer_list):
            l = len(person)
            assert l not in previous_answers and 0 <= l <= 8
            previous_answers.append(l)
            if index != 0:
                if index % 2 == 0: partner = index -1
                else: partner = index +1
                assert partner not in person
    except AssertionError:
        return False
    return True

def gen_perm_unique_values(pool: list, length, cur=[]):
    if len(cur) >= length:
        yield cur  # yields one permutation
        return True
    for n in range(pool_length := len(pool)):
        cur.append(pool.pop(0))  # next value of current digit
        # calls for following digits to be generated
        yield from gen_perm_unique_values(pool, length)
        pool.append(cur.pop())  # prepares for next value of current digit

def test_unique_perm_function():
    def faculty(n: int):
        if n == 0:
            return 1
        return n*faculty(n-1)

    assert faculty(4) == 24
    assert faculty(0) == 1

    count = 0
    test_list = list(range(10))
    length_of_perm = 5
    assert length_of_perm <= len(test_list)
    for p in gen_perm_unique_values(test_list.copy(), length_of_perm):
        count += 1
        # print(p)
        for v in p:
            assert p.count(v) == 1
    assert count == faculty(len(test_list))/faculty(len(test_list)-length_of_perm) 
test_unique_perm_function()

#Conclusion: this riddle is simply not fit to solve like this. The solution to the riddle has nothing to do with which person one actually interacted with.