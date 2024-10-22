from cards import *
from poker_combination import PokerCombination
from distribution import distribution
from random import randint as ri

"""
____________________________________________________T_E_S_T_____________________________________________________________

        You can choose how many players will be in game. Each player has random amount of chips and goes all-in.
________________________________________________________________________________________________________________________
"""

# __________________________________________FOR_BETTER_VISUALISING______________________________________________________

SUITS_SYMBOLS = ("♥", "♦", "♠", "♣")
CARD_VALUES_SYMBOLS = (" 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", " J", " Q", " K", " A")


def print_cards(*cards):
    for card in cards:
        print(CARD_VALUES_SYMBOLS[card.value], SUITS_SYMBOLS[card.suit], end=" ")


# ______________________________________________THE_GAME_ITSELF_________________________________________________________


deck = Deck()
number_of_players = int(input("Enter number of players (0 < x < 24): "))
table = [deck.draw() for _ in range(5)]
total_bets = [ri(0, 1000) for _ in range(number_of_players)]
players_hands = [[deck.draw() for _ in range(2)] for _ in range(number_of_players)]
players_combos = [PokerCombination(players_hands[player] + table) for player in range(number_of_players)]


print("TABLE: ", end=" ")
print_cards(*table)
print(f" (total bank {sum(total_bets)})")
for n, hand in enumerate(players_hands):
    print(f"{"0" if n < 9 else ""}{n+1}.    ", end=" ")
    print_cards(*hand)
    print(f"     BET: {total_bets[n]}, COMBINATION: {players_combos[n].name}")


distribution_results = distribution(players_combos, total_bets)
print(list(map(int, distribution_results)), f"({int(sum(distribution_results))} total distributed)")

# ______________________________________________________________________________________________________________________
