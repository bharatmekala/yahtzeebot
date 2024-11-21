import itertools
import json

class Player:
    def __init__(self, name):
        self.name = name
        self.scorecard = {
            "ones": None, "twos": None, "threes": None, "fours": None, "fives": None, "sixes": None,
            "three_of_a_kind": None, "four_of_a_kind": None, "full_house": None, "small_straight": None,
            "large_straight": None, "yahtzee": None, "chance": None
        }
        self.total_score = 0
        with open('lookup_tables/ev_lookup_table.json', 'r') as f:
            self.ev_lookup_table = json.load(f)

    def decide_keep_or_end(self, dice):
        print(f"Dice: {dice}")
        choice = input(f"{self.name}, enter dice to keep (e.g., 0 2 3), 'roll' to roll again, or 'end' to end your turn: ").strip()
        if choice == "roll":
            return "roll", []
        elif choice == "end":
            return "end", []
        else:
            keep = [int(x) for x in choice.split()]
            return "keep", keep

    def choose_category(self, dice):
        print(f"Dice: {dice}")
        category = input(f"{self.name}, choose a category to score: ").strip().lower()
        return category

    def display_scorecard(self):
        print(f"{self.name}'s Scorecard:")
        for category, score in self.scorecard.items():
            print(f"{category.capitalize()}: {score if score is not None else '---'}")
        print(f"Total Score: {self.total_score}\n")
    
    #helper function to calculate score for each category
    def calculate_score(self, dice, category):
        counts = {x: dice.count(x) for x in range(1, 7)}
        if category == "ones":
            return counts[1] * 1
        elif category == "twos":
            return counts[2] * 2
        elif category == "threes":
            return counts[3] * 3
        elif category == "fours":
            return counts[4] * 4
        elif category == "fives":
            return counts[5] * 5
        elif category == "sixes":
            return counts[6] * 6
        elif category == "three_of_a_kind":
            return sum(dice) if max(counts.values()) >= 3 else 0
        elif category == "four_of_a_kind":
            return sum(dice) if max(counts.values()) >= 4 else 0
        elif category == "full_house":
            return 25 if sorted(counts.values(), reverse=True)[:2] == [3, 2] else 0
        elif category == "small_straight":
            return 30 if any(set(range(start, start + 4)).issubset(dice) for start in range(1, 4)) else 0
        elif category == "large_straight":
            return 40 if set(range(1, 6)).issubset(dice) or set(range(2, 7)).issubset(dice) else 0
        elif category == "yahtzee":
            return 50 if max(counts.values()) == 5 else 0
        elif category == "chance":
            return sum(dice)
        else:
            return 0
    
    def calculate_ev(self, dice, category):
        dice_tuple = tuple(sorted(dice))
        dice_key = str(dice_tuple)
        return self.ev_lookup_table[dice_key][category]
