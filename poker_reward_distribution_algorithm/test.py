from cards import *
from poker_combination import PokerCombination
from distribution import distribution

"""
_____________________________________________TEST_YOUR_CUSTOM_LAYOUTS___________________________________________________
"""

table = [
    Card(12, 2),
    Card(11, 2),
    Card(10, 3),
    Card(9, 1),
    Card(8, 1),
]

hand1 = [Card(6, 2), Card(11, 0)]
hand2 = [Card(2, 0), Card(4, 0)]

total_bets = [874, 26]
combos = [PokerCombination(hand1 + table), PokerCombination(hand2 + table)]

for c in combos:
    print(c.power)

distribution_results = distribution(combos, total_bets)
print(distribution_results)
