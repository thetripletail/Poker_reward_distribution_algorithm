def distribution(combos, bets):
    # COMBOS[INDEX] AND BETS[INDEX] MUST POINT TO THE SAME PLAYER

    number_of_players = len(combos)
    distributed = [0 for _ in range(number_of_players)]

    # ADDING PLAYER INDEXES TO EACH COMBO
    indexed_combos = [i for i in enumerate(combos)]
    # SORTING IT BY SELF POWER
    indexed_combos.sort(key=lambda x: x[1].power, reverse=True)

    # GROUPING PLAYERS INDEXES INTO TOP (IF PLAYERS COMBOS POWER ARE EQUAL THEY SHARE ONE PLACE IN TOP)_________________
    top = [[indexed_combos[0][0]]]
    for i in range(1, len(indexed_combos)):
        if indexed_combos[i][1].power == indexed_combos[i - 1][1].power:
            top[-1].append(indexed_combos[i][0])
        else:
            # SORTING ONE-PLACE-SHARING PLAYERS-INDEXES BY THEIR BETS (ASCENDING)
            top[-1].sort(key=lambda x: bets[x])
            top.append([indexed_combos[i][0]])
    top[-1].sort(key=lambda x: bets[x])
    # __________________________________________________________________________________________________________________

    # print(top)  # <--- UNCOMMENT THIS FOR VIEWING THE TOP

    for place in top:
        for n, i in enumerate(place):   # i = PLAYER'S INDEX
            # HOW MANY PLAYERS-IN-TOP LEFT TO SHARE BETWEEN
            share = len(place) - n
            # CURRENT REMINDER OF i-PLAYER'S BET
            bet = bets[i]
            reward = 0
            for j in range(number_of_players):
                # CHECKING BET REMINDER OF PLAYERS WHO DON'T SHARE CURRENT PLACE
                if j not in place:
                    # loss IS A MINIMUM BETWEEN BET REMINDERS OF i-PLAYER("WINNER") AND j-PLAYER("LOSER")
                    loss = min(bets[j], bet)
                    # ADDING A LOSS DIVIDED BY PLAYERS-IN-TOP TO reward
                    reward += loss / share
                    # TAKING LOST CHIPS FROM LOSER
                    bets[j] -= loss
            # ADDING REWARD TO PLAYERS-IN-TOP LEFT
            for m in range(1, share+1):
                winner_index = place[-m]
                # SUBTRACT i-PLAYER BET REMINDER FROM THEM
                bets[winner_index] -= bet
                # ADDING REWARD TO distributed BY THEIR PLAYER-INDEXES
                distributed[winner_index] += reward + bet
    # bets-LIST MUST CONTAIN ONLY ZEROS IF EVERYTHING WENT CORRECTLY
    # print(bets)   # <--- UNCOMMENT THIS TO CHECK
    return distributed
