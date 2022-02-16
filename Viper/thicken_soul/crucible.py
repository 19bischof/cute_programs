import thai
from tqdm import tqdm

# the following are simply time optimizations
# there are a lot more optimizations that could be done
thai.cons = False
thai.no_early_finish_check = True
thai.log_it = False
thai.logging.getLogger().setLevel(thai.logging.WARNING)

def one_game(methods):
    i = thai.p_index
    fin = False
    while not fin:
        methods[i]()
        i = (i + 1) % len(methods)
        fin = thai.finished()
    if fin.find("1") != -1:
        return 0
    if fin.find("2") != -1:
        return 1
    return -1


methods = {0: thai.bot0_angela, 1: thai.bot0_angela}
results = []
iterations = 30000
for i in tqdm(range(iterations)):
    results.append(one_game(methods))
    thai.reset_game()
print("0:    {:05.2f}%".format(100 * results.count(0) / iterations))
print("1:    {:05.2f}%".format(100 * results.count(1) / iterations))
print("draw: {:05.2f}%".format(100 * results.count(-1) / iterations))
