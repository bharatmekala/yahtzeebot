import random
from bot import Bot

class RandomBot1(Bot):
    def __init__(self):
        super().__init__("RandomBot")

    def decide_keep_or_end(self, dice):
        action = random.choice(["roll", "end"])
        if action == "roll":
            keep = random.sample(range(5), random.randint(0, 5))
            return "roll", keep
        else:
            return "end", []

    def choose_category(self, dice):
        available_categories = [category for category, score in self.scorecard.items() if score is None]
        return random.choice(available_categories)


class RandomBot2(Bot):
    def __init__(self):
        super().__init__("RandomBot")

    def decide_keep_or_end(self, dice):
        keep = random.sample(range(5), random.randint(0, 5))
        if not keep:
            return "end", []
        else:
            return "roll", keep

    def choose_category(self, dice):
        available_categories = [category for category, score in self.scorecard.items() if score is None]
        return random.choice(available_categories)
