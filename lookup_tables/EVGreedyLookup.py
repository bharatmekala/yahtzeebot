import itertools
import json

with open('lookup_tables/ev_lookup_table.json', 'r') as f:
    ev_lookup_table = json.load(f)

def generate_best_subset_lookup_table():
    categories = ["ones", "twos", "threes", "fours", "fives", "sixes", "three_of_a_kind", "four_of_a_kind", "full_house", "small_straight", "large_straight", "yahtzee", "chance"]
    lookup_table = {}

    for dice in itertools.product(range(1, 7), repeat=5):
        dice_tuple = tuple(sorted(dice))
        for r in range(1, len(categories) + 1):
            for available_categories in itertools.combinations(categories, r):
                key = (dice_tuple, available_categories)
                lookup_table[str(key)] = best_subset_to_keep(dice, available_categories)

    with open('lookup_tables/best_subset_lookup_table.json', 'w') as f:
        json.dump(lookup_table, f)

def best_subset_to_keep(dice, available_categories):
    best_ev = -1
    best_subset = []
    # Generate all possible combinations of dice to keep
    for r in range(6):  # 0 to 5 dice can be kept
        for subset in itertools.combinations(range(5), r):
            kept_dice = [dice[i] for i in subset]
        
            # Calculate the expected value across all categories
            ev = sum(calculate_ev(kept_dice, category) for category in available_categories) / len(available_categories)
        
            if ev > best_ev:
                best_ev = ev
                best_subset = subset

    return list(best_subset)

def calculate_ev(dice, category):
    dice_tuple = tuple(sorted(dice))
    dice_key = str(dice_tuple)
    return ev_lookup_table[dice_key][category]
    

# Generate the lookup table
generate_best_subset_lookup_table()
