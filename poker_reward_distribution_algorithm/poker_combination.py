class PokerCombination:

    COMBINATION_NAMES = {
        0: "High card",
        1: "Pair",
        2: "Two pairs",
        3: "Set",
        4: "Straight",
        5: "Flush",
        6: "Full-House",
        7: "Quads",
        8: "Straight-Flush",
        9: "Royal-Flush"
    }

    def __init__(self, cards):
        if not (2 <= len(cards) <= 7):
            raise Exception(f"Invalid cards length({len(cards)})")
        self.cards = cards
        self.power, self.combination = self.get_combination_info()
        self.name = self.COMBINATION_NAMES[self.power]
        self._add_seniority()

    def get_combination_info(self):
        # RETURNS MAJOR POWER OF THE COMBINATION AND <=5 CORRECTLY SORTED CARDS OF ITSELF
        values_sorted = sorted(self.cards, key=lambda card: card.value)
        result = self.check_on_straight_and_flushes(values_sorted)
        # IF NOT STRAIGHT-FLUSH CHECK NEXT
        if result[0] < 8:
            new_result = self.check_on_groups(self.group_by_value(values_sorted))
            result = new_result if new_result[0] > result[0] else result
            # IF NOT ANY COMBINATION GO TO RETURN "HIGH CARD"
            if result[0] == 0:
                result = self.high_card(values_sorted)
        return result

    """
    "SENIORITY" IS AN IDENTIFIER THAT NEEDS TO COMPARE COMBINATIONS WITH EQUAL MAJOR POWER
    EXAMPLES: 
                    TWO PAIRS (A, A, 2, 2, 3) > (K, K, Q, Q, J) TWO PAIRS
                        HIGH CARD (10, 2) > (9, 8, 7, 6, 4) HIGH CARD
                           HIGH CARD (10, 3) < (10, 3, 2) HIGH CARD
    """
    def _add_seniority(self):
        seniority = 0
        # SIMILAR TO CONVERT BASE-FOURTEEN NUMBER (0-13 CARD VALUES, ZERO IS NO-CARD) INTO DECIMAL
        for i in range(len(self.combination)):
            seniority += (self.combination[i].value + 1) * (14 ** (5-i))
        # self.power BECOMING A TUPLE FOR COMPARISON ( (MAJOR POWER, SENIORITY) )
        self.power = self.power, seniority

    @staticmethod
    def group_by_value(cards):
        # RETURNS LEN-13 LIST OF CARDS GROPED BY VALUES (EACH INDEX == VALUES OF CARDS IN IT)
        sorted_cards = [[] for _ in range(13)]
        for card in cards:
            sorted_cards[card.value].append(card)
        return sorted_cards

    @staticmethod
    def group_by_suits(cards):
        # RETURNS LEN-4 LIST OF CARDS GROPED BY SUITS (EACH INDEX == SUIT OF CARDS IN IT)
        sorted_cards = [[], [], [], []]
        for card in cards:
            sorted_cards[card.suit].append(card)
        return sorted_cards

    @staticmethod
    def check_on_straight_and_flushes(cards):
        if len(cards) >= 5:
            suit_groups = PokerCombination.group_by_suits(cards)
            # CHECK_ON_FLUSHES
            for group in suit_groups:
                if len(group) >= 5:
                    straight = PokerCombination.check_on_straight(group)
                    # CHECK_ON_STRAIGHT-FLUSH
                    if len(straight) == 5:
                        # COMMON
                        if straight[0].value < 12:
                            return 8, straight
                        # ROYAL
                        else:
                            return 9, straight
                    # RETURN FLUSH
                    else:
                        group.reverse()
                        while len(group) > 5:
                            group.pop(-1)
                        return 5, group
            straight = PokerCombination.check_on_straight(cards)
            # CHECK_ON_STRAIGHT
            if len(straight) == 5:
                return 4, straight
        # NO "STRAIGHT OR FLUSH" COMBINATION
            return 0,
        else:
            return 0,

    @staticmethod
    # NOTICE: 5-4-3-2-A COMBINATION DOES NOT COUNT AS STRAIGHT
    def check_on_straight(cards):
        # CURRENT HIGHEST CARD OF STRAIGHT
        i = len(cards) - 1
        # CURRENT LOWEST CARD OF STRAIGHT
        j = i - 1
        # CURRENT VALUE DIFFERENCE BETWEEN HIGHEST AND LOWEST CARD OF STRAIGHT
        k = 0
        # CURRENT STRAIGHT COLLECTION
        straight = [cards[i]]
        while i >= 4 and len(straight) < 5 and j >= 0:
            # DIFFERENCE BETWEEN i- AND j- CARDS
            dif = cards[i].value - cards[j].value
            # CONTINUE CURRENT STRAIGHT BY ADDING j-CARD
            if dif == 1 + k:
                straight.append(cards[j])
                k += 1
            # RESET CURRENT STRAIGHT
            elif dif > 1 + k:
                i = j
                straight = [cards[i]]
                k = 0
            # ELSE CONTINUE CURRENT STRAIGHT
            j -= 1
        return straight

    @staticmethod
    def check_on_groups(cards):
        # ____________SOLOS__PAIRS__TRIPLES__QUADS__
        groups = [[], [   ], [   ], [     ], [   ]]
        combo = []
        for group in cards:
            groups[len(group)].append(group)

        # ___________________________________IF_FROM_FIVE_TO_SEVEN_CARDS_WERE_GIVEN_____________________________________
        if len(cards) >= 5:
            # CHECK ON QUADS
            if len(groups[4]) == 1:
                combo.extend(groups[4][-1])
                # 4-3
                if len(groups[3]) == 1:
                    combo.append(groups[3][-1][-1])
                # 4-2-1 AND PAIR'S CARD VALUE IS HIGHER THAN SOLO CARD VALUE
                elif len(groups[2]) == 1 and groups[1][-1][-1].value < groups[2][-1][-1].value:
                    combo.append(groups[2][-1][-1])
                # 4-1-1-1 / (4-2-1 AND PAIR'S CARD VALUE IS LESSER THAN SOLO CARD VALUE)
                else:
                    combo.extend(groups[1][-1])
                return 7, combo
            # CHECK ON SET / FULL-HOUSE
            if len(groups[3]) > 0:
                combo.extend(groups[3][-1])
                # 3-2-2 / 3-2-1-1
                if len(groups[2]) > 0:
                    combo.extend(groups[2][-1])
                    return 6, combo
                else:
                    # 3-1-1-1-1
                    if len(groups[3]) < 2:
                        combo.extend(groups[1][-1])
                        combo.extend(groups[1][-2])
                        return 3, combo
                    # 3-3-1
                    else:
                        combo.append(groups[3][-2][-1])
                        combo.append(groups[3][-2][-2])
                    return 6, combo
            # CHECK ON PAIR / TWO PAIRS
            if len(groups[2]) > 0:
                # 2-2-1-1-1
                if len(groups[2]) > 1:
                    combo.extend(groups[2][-1])
                    combo.extend(groups[2][-2])
                    combo.extend(groups[1][-1])
                    return 2, combo
                # 2-1-1-1-1-1
                else:
                    combo.extend(groups[2][-1])
                    combo.extend(groups[1][-1])
                    combo.extend(groups[1][-2])
                    combo.extend(groups[1][-3])
                    return 1, combo
            # NO "GROUPS" COMBINATION
            return 0,

        # ___________________________________________IF_FOUR_CARDS_WERE_GIVEN___________________________________________
        elif len(cards) == 4:
            # 4-0
            if len(groups[4]) == 1:
                combo.extend(groups[4][-1])
                return 7, combo
            # 3-1
            if len(groups[3]) == 1:
                combo.extend(groups[3][-1])
                combo.extend(groups[1][-1])
                return 3, combo
            # 2-2
            if len(groups[2]) == 2:
                combo.extend(groups[2][-1])
                combo.extend(groups[2][-2])
                return 2, combo
            # 2-1-1
            if len(groups[2]) == 1:
                combo.extend(groups[2][-1])
                combo.extend(groups[1][-1])
                combo.extend(groups[1][-2])
                return 1, combo
            # NO "GROUPS" COMBINATION
            return 0,

        # __________________________________________IF_THREE_CARDS_WERE_GIVEN___________________________________________
        elif len(cards) == 3:
            # 3-0
            if len(groups[3]) == 1:
                combo.extend(groups[3][-1])
                return 3, combo
            # 2-1
            if len(groups[2]) == 1:
                combo.extend(groups[2][-1])
                combo.extend(groups[1][-1])
                return 1, combo
            # NO "GROUPS" COMBINATION
            return 0,

        # ____________________________________________IF_TWO_CARDS_WERE_GIVEN___________________________________________
        # 2-0
        elif len(cards) == 2 and len(groups[2]) == 1:
            combo.extend(groups[2][-1])
            return 1, combo

        # ____________________________________________IF_ONE_CARD_WAS_GIVEN____________________________________________
        return 0,

    @staticmethod
    def high_card(cards):
        combo = []
        n = min(5, len(cards))
        for i in range(1, n+1):
            combo.append(cards[-i])
        return 0, combo
