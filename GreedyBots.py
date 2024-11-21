import random
import itertools
from bot import Bot

class RandomGreedyBot(Bot):
    def __init__(self):
        super().__init__("GreedyBot")

    def decide_keep_or_end(self, dice):
        keep = random.sample(range(5), random.randint(0, 5))
        if not keep:
            return "end", []
        else:
            return "roll", keep

    def choose_category(self, dice):
        available_categories = [category for category, score in self.scorecard.items() if score is None]
        best_category = None
        best_score = -1

        for category in available_categories:
            score = self.calculate_score(dice, category)
            if score > best_score:
                best_score = score
                best_category = category

        return best_category

class EVGreedyBot(Bot):
    def __init__(self):
        super().__init__("GreedyBot")

    def decide_keep_or_end(self, dice):
        keep = self.best_subset_to_keep(dice, [category for category, score in self.scorecard.items() if score is None])
        if not keep:
            return "end", []
        else:
            return "roll", keep
    

    def choose_category(self, dice):
        available_categories = [category for category, score in self.scorecard.items() if score is None]
        best_category = None
        best_score = -1

        for category in available_categories:
            score = self.calculate_score(dice, category)
            if score > best_score:
                best_score = score
                best_category = category

        return best_category
    
    def best_subset_to_keep(self, dice, available_categories):
        best_ev = -1
        best_subset = []
        # Generate all possible combinations of dice to keep
        for r in range(6):  # 0 to 5 dice can be kept
            for subset in itertools.combinations(range(5), r):
                kept_dice = [dice[i] for i in subset]
            
                # Calculate the expected value across all categories
                ev = sum(self.calculate_ev(kept_dice, category) for category in available_categories) / len(available_categories)
            
                if ev > best_ev:
                    best_ev = ev
                    best_subset = subset
    
        return list(best_subset)

class MAXGreedyBot(EVGreedyBot):
    def __init__(self):
        super().__init__()
    
    def best_subset_to_keep(self, dice, available_categories):
        best_ev = -1
        best_subset = []
        # Generate all possible combinations of dice to keep
        for r in range(6):  # 0 to 5 dice can be kept
            for subset in itertools.combinations(range(5), r):
                kept_dice = [dice[i] for i in subset]
            
                # Calculate the expected value across all categories
                ev = max(self.calculate_ev(kept_dice, category) for category in available_categories) / len(available_categories)
            
                if ev > best_ev:
                    best_ev = ev
                    best_subset = subset
    
        return list(best_subset)

class EpsilonGreedyBot(EVGreedyBot):
    def __init__(self, epsilon=0.1):
        super().__init__()
        self.epsilon = epsilon

    def best_subset_to_keep(self, dice, available_categories):
        if random.random() < self.epsilon:
            # With probability epsilon, act like MAXGreedyBot
            best_ev = -1
            best_subset = []
            # Generate all possible combinations of dice to keep
            for r in range(6):  # 0 to 5 dice can be kept
                for subset in itertools.combinations(range(5), r):
                    kept_dice = [dice[i] for i in subset]
                    # Max EV over all categories
                    ev = max(self.calculate_ev(kept_dice, category) for category in available_categories)
                    if ev > best_ev:
                        best_ev = ev
                        best_subset = subset
            return list(best_subset)
        else:
            # With probability 1 - epsilon, act like EVGreedyBot
            return super().best_subset_to_keep(dice, available_categories)

class TaperingBot(EVGreedyBot):
    def __init__(self):
        super().__init__()
        self.round = 0  # Initialize round counter

    def best_subset_to_keep(self, dice, available_categories):
        # Increment round counter
        self.round += 1

        if self.round <= 6:
            # Use MAXGreedy strategy in rounds 1-6
            best_ev = -1
            best_subset = []
            for r in range(6):  # 0 to 5 dice can be kept
                for subset in itertools.combinations(range(5), r):
                    kept_dice = [dice[i] for i in subset]
                    # Max EV over all categories
                    ev = max(self.calculate_ev(kept_dice, category) for category in available_categories)
                    if ev > best_ev:
                        best_ev = ev
                        best_subset = subset
            return list(best_subset)
        else:
            # Use EVGreedy strategy in rounds 7-13
            return super().best_subset_to_keep(dice, available_categories)


