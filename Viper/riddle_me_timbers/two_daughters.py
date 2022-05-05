import random,tqdm
iterations = 10_000_000
boys,girls = 0,0
for i in tqdm.tqdm(range(iterations)):
    while random.random() > 0.5: # if got a boy -> continue sexing
        boys += 1
    girls += 1 #eventually got a girl
print(f"boys: {100*boys/(boys+girls):.0f} %\t girls: {100*girls/(boys+girls):.0f}")

"""King Nupe of the kingdom Catan dotes on his two daughters so much that he decides the kingdom would be better off with more girls than boys, and he makes the following decree:
All child-bearing couples must continue to bear children until they have a daughter!
But to avoid overpopulation, he makes an additional decree:
All child-bearing couples will stop having children once they have a daughter!
His subjects immediately begin following his orders.
After many years, what's the expected ratio of girls to boys in Catan?"""