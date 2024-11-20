from player import Player

class Bot(Player):
    def __init__(self, name):
        super().__init__(name)
        # can see self.name, self.scorecard, self.total_score

    def decide_keep_or_end(self, dice):
        """
        The bot decides which dice to keep or whether to end the turn.
        :param dice: List of current dice values.
        :return: Tuple ("roll"/"keep"/"end", indices of dice to keep).
        """

    def choose_category(self, dice):
        """
        The bot chooses a scoring category based on the dice.
        :param dice: List of final dice values.
        :return: Selected category as a string.
        """

#categories for ref
categories = [
    "ones",
    "twos",
    "threes",
    "fours",
    "fives",
    "sixes",
    "three_of_a_kind",
    "four_of_a_kind",
    "full_house",
    "small_straight",
    "large_straight",
    "yahtzee",
    "chance"
]

