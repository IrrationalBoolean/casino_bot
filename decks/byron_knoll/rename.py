import glob
my_dict = dict(**{str(x) : str(x) for x in range(2, 11)}, **{"king": "K", "queen": "Q", "jack": "J", "ace":"A"})
print(my_dict)
import os

for x in glob.glob('*'):
    if x.endswith('.png'):
        c = x.split('_')
        card = ''.join([c[-1][0].upper(), my_dict.get(c[0], ''), '.png'])
        os.rename(x, card)
        print(card)

