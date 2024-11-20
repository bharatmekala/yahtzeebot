import itertools

class Player:
    def __init__(self, name):
        self.name = name
        self.scorecard = {
            "ones": None, "twos": None, "threes": None, "fours": None, "fives": None, "sixes": None,
            "three_of_a_kind": None, "four_of_a_kind": None, "full_house": None, "small_straight": None,
            "large_straight": None, "yahtzee": None, "chance": None
        }
        self.total_score = 0

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
        # Shortcuts for certain categories to avoid full enumeration
        if len(dice) < 5:
            # Ones through Sixes have predictable EV
            if category in ["ones", "twos", "threes", "fours", "fives", "sixes"]:
                num = {"ones": 1, "twos": 2, "threes": 3, "fours": 4, "fives": 5, "sixes": 6}[category]
                missing_dice = 5 - len(dice)
                current_count = dice.count(num)
                return ((current_count + (missing_dice * (1/6))) * num)

         # Chance has a simple linear expectation
            if category == "chance":
                missing_dice = 5 - len(dice)
                return sum(dice) + (missing_dice * 3.5)

            # For more complex categories, use full enumeration
            total_ev = 0
            missing_dice = 5 - len(dice)
            for roll_combination in itertools.product(range(1, 7), repeat=missing_dice):
                full_dice = list(dice) + list(roll_combination)
                score = self.calculate_score(full_dice, category)
                prob = 1 / (6 ** missing_dice)
                total_ev += score * prob
        
            return total_ev

        # If 5 dice, simply return the score
        return self.calculate_score(dice, category)
    
    

