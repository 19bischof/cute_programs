# logic riddle from https://www.popularmechanics.com/science/math/a31153757/riddles-brain-teasers-logic-puzzles/
# Carol was creating a family tree, but had trouble tracking down her mother's birthdate.
# The only clue she found was a letter written from her grandfather to her grandmother on the day
# her mother was born. Unfortunately, some of the characters were smudged out, represented here with a "___".
# (The length of the line does not reflect the number of smudged characters.)
# "Dear Virginia, Little did I know when I headed to work this Monday morning, that by evening
# we would have a beautiful baby girl. And on our wedding anniversary, no less! It makes me think
# back to that incredible weekend day, J___ 27th, 19___, when we first shared our vow to create
# a family together, and, well, here we are! Happy eighth anniversary, my love. Love, Edwin"
# The question: When was Carol's mother born?
import datetime
current_date = datetime.date(1900, 1, 1)
end_date = datetime.date(2000, 1, 1)
count = 0
winner = []


def _print(*args):
    global count
    count += 1
    print(*args)


def check(date: datetime.date):
    if date.day == 27:
        _print(f"{count:03d}: days match")
        if date.month in (1, 6, 7):
            _print(f"{count:03d}: months match")
            if date.weekday() in (5, 6):
                _print(f"{count:03d}: weekdays match")
                assert 1900 <= date.year < 2000
                eight_years = date.year + 8
                new_date = datetime.date(eight_years, date.month, date.day)
                if new_date.weekday() == 0:
                    _print(f"{count:3d}: someone won")
                    winner.append((date, new_date))


one_day = datetime.timedelta(days=1)
while (current_date < end_date):
    check(current_date)
    current_date += one_day

assert len(winner) == 1
print("a match was found at", winner[0][0])
print("The eigth anniversary was celebrated at", winner[0][1])
