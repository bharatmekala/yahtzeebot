import itertools
import json

def generate_ev_lookup_table():
    categories = ["ones", "twos", "threes", "fours", "fives", "sixes", "three_of_a_kind", "four_of_a_kind", "full_house", "small_straight", "large_straight", "yahtzee", "chance"]
    lookup_table = {}

    for category in categories:
        for length in range(0, 6):  # Iterate over lengths from 1 to 5
            for dice in itertools.product(range(1, 7), repeat=length):
                dice_tuple = tuple(sorted(dice))
                dice_key = str(dice_tuple)  # Convert tuple to string
                if dice_key not in lookup_table:
                    lookup_table[dice_key] = {}
                lookup_table[dice_key][category] = calculate_ev(dice, category)

    with open('ev_lookup_table.json', 'w') as f:
        json.dump(lookup_table, f)

def calculate_ev(dice, category):
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
                score = calculate_score(full_dice, category)
                prob = 1 / (6 ** missing_dice)
                total_ev += score * prob
        
            return total_ev

        # If 5 dice, simply return the score
        return calculate_score(dice, category)

def calculate_score(dice, category):
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

# Generate the lookup table
generate_ev_lookup_table()
