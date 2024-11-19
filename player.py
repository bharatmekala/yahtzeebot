class Player:
    def __init__(self, name):
        self.name = name
        self.scorecard = {}
        self.total_score = 0

    def add_score(self, category, score):
        if category in self.scorecard:
            print(f"{self.name} has already scored in {category}.")
            return False
        self.scorecard[category] = score
        self.total_score += score
        return True

    def display_scorecard(self):
        print(f"{self.name}'s Scorecard:")
        for category, score in self.scorecard.items():
            print(f"{category.capitalize()}: {score}")
        print(f"Total Score: {self.total_score}\n")

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
        print(f"Final dice: {dice}")
        return input(f"{self.name}, enter a scoring category: ").strip().lower()
