import random
from player import Player

class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.dice = [0] * 5
        self.current_player_index = 0
        self.rolls_left = 3

    def roll_dice(self, keep=[]):
        for i in range(5):
            if i not in keep:
                self.dice[i] = random.randint(1, 6)
        self.rolls_left -= 1

    def calculate_score(self, category):
        counts = {x: self.dice.count(x) for x in range(1, 7)}
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
            return sum(self.dice) if max(counts.values()) >= 3 else 0
        elif category == "four_of_a_kind":
            return sum(self.dice) if max(counts.values()) >= 4 else 0
        elif category == "full_house":
            return 25 if sorted(counts.values(), reverse=True)[:2] == [3, 2] else 0
        elif category == "small_straight":
            return 30 if any(set(range(start, start + 4)).issubset(self.dice) for start in range(1, 4)) else 0
        elif category == "large_straight":
            return 40 if set(range(1, 6)).issubset(self.dice) or set(range(2, 7)).issubset(self.dice) else 0
        elif category == "yahtzee":
            return 50 if max(counts.values()) == 5 else 0
        elif category == "chance":
            return sum(self.dice)
        else:
            print("Invalid category!")
            return 0

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.rolls_left = 3
        self.dice = [0] * 5

    def run_game(self):
        rounds = 13
        for _ in range(rounds):
            for player in self.players:
                print(f"\n{player.name}'s turn!")
                self.rolls_left = 3
                keep = []

                while self.rolls_left > 0:
                    self.roll_dice(keep)
                    print(f"Dice: {self.dice}")
                    action, keep = player.decide_keep_or_end(self.dice)

                    if action == "end":
                        break

                category = player.choose_category(self.dice)
                score = self.calculate_score(category)
                if player.add_score(category, score):
                    print(f"{player.name} scored {score} points in {category}!")
                self.next_player()

        self.display_final_scores()

    def display_final_scores(self):
        print("\nFinal Scores:")
        for player in self.players:
            player.display_scorecard()

        winner = max(self.players, key=lambda p: p.total_score)
        print(f"The winner is {winner.name} with {winner.total_score} points!")


# Example usage
game = Game(["Alice", "Bob"])
game.run_game()
