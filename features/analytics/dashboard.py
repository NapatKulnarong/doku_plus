import csv
import os
from collections import Counter
from features.analytics import graph_generator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE = os.path.join(BASE_DIR, "data", "game_stats.csv")


def load_data(filename):
    """Load data from CSV file."""
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print("No game data found.")
        return []


def summarize(data):
    """Summarize data."""
    if not data:
        print("No data to analyze.")
        return

    total_games = len(data)
    wins = sum(1 for row in data if row["Win"] == "Win")
    losses = total_games - wins
    avg_mistakes = sum(int(row["Mistakes"]) for row in data) / total_games
    avg_hints = sum(int(row["Hints Used"]) for row in data) / total_games
    avg_user_cells = sum(int(row.get("Filled Cells", 0)) for row in data) / total_games

    print(f"Total Games: {total_games}")
    print(f"Wins: {wins}, Losses: {losses}")
    print(f"Win Rate: {wins / total_games * 100:.2f}%")
    print(f"Average Mistakes: {avg_mistakes:.2f}")
    print(f"Average Hints Used: {avg_hints:.2f}")
    print(f"Average User Filled Cells: {avg_user_cells:.2f}")

    # Difficulty breakdown
    difficulties = Counter(row["Difficulty"] for row in data)
    print("Games by Difficulty:")
    for difficulty, count in difficulties.items():
        print(f"  {difficulty}: {count}")


def main():
    """Main function to generate graphs and stats."""
    data = load_data(DATA_FILE)
    summarize(data)

    # Generate graphs
    graph_generator.generate_time_played_line_graph(data)
    graph_generator.generate_mistakes_bar_chart(data)
    graph_generator.generate_win_loss_pie_chart(data)
    graph_generator.generate_hints_usage_pie_chart(data)
    graph_generator.generate_time_per_difficulty_boxplot(data)
    graph_generator.generate_correlation_matrix(data)
    graph_generator.generate_time_statistics_table(data)


if __name__ == "__main__":
    main()