import matplotlib.pyplot as plt
from game import Game
from RandomBots import RandomBot1, RandomBot2
from GreedyBots import RandomGreedyBot, EVGreedyBot, MAXGreedyBot, EpsilonGreedyBot, TaperingBot
import numpy as np
import os
from tqdm import tqdm

def test_bot(bot_class, num_games=10000, output_dir="output"):
    scores = []
    category_scores = {category: [] for category in [
        "ones", "twos", "threes", "fours", "fives", "sixes",
        "three_of_a_kind", "four_of_a_kind", "full_house",
        "small_straight", "large_straight", "yahtzee", "chance"
    ]}

    for _ in tqdm(range(num_games), desc="Running games"):
        game = Game([bot_class])
        game.run_game()
        scores.append(game.players[0].total_score)
        for category, score in game.players[0].scorecard.items():
            if score is not None:
                category_scores[category].append(score)

    # Calculate average scores for each category
    avg_category_scores = {category: np.mean(scores) if scores else 0 for category, scores in category_scores.items()}
    avg_total_score = np.mean(scores)

    # Print the average total score
    print(f'Average Total Score for {bot_class.__name__} over {num_games} Games: {avg_total_score:.2f}')

    # Print the average scores for each category
    print(f'Average Scores for Each Category for {bot_class.__name__} over {num_games} Games:')
    for category, avg_score in avg_category_scores.items():
        print(f'{category.capitalize()}: {avg_score:.2f}')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Plot the total scores
    plt.hist(scores, bins=20, edgecolor='black')
    plt.title(f'Scores Distribution for {bot_class.__name__} over {num_games} Games')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, f'{bot_class.__name__}_scores_distribution.png'))
    plt.close()

    # Plot the average scores for each category
    categories = list(avg_category_scores.keys())
    avg_scores = list(avg_category_scores.values())

    plt.bar(categories, avg_scores, edgecolor='black')
    plt.title(f'Average Scores for Each Category for {bot_class.__name__} over {num_games} Games')
    plt.xlabel('Category')
    plt.ylabel('Average Score')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()  # Adjust layout to make room for the rotated labels
    plt.savefig(os.path.join(output_dir, f'{bot_class.__name__}_average_scores.png'))
    plt.close()

# Example usage
test_bot(TaperingBot)
