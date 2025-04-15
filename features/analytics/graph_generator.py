import matplotlib
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
matplotlib.use('TkAgg')

# Helper to convert time string 'mm:ss' to total seconds
def time_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60 + seconds
    except Exception:
        return 0

# 1️⃣ Time Played — Line Graph
def generate_time_played_line_graph(data):
    times = [time_to_seconds(row['Time']) for row in data]
    plt.figure()
    plt.plot(range(1, len(times) + 1), times, marker='o')
    plt.title('Completion Time per Session')
    plt.xlabel('Session Number')
    plt.ylabel('Time (seconds)')
    plt.grid(True)
    plt.show()

# 2️⃣ Mistakes per Difficulty — Bar Chart
def generate_mistakes_bar_chart(data):
    difficulty_mistakes = defaultdict(list)
    for row in data:
        difficulty_mistakes[row['Difficulty']].append(int(row['Mistakes']))

    difficulties = list(difficulty_mistakes.keys())
    avg_mistakes = [sum(values) / len(values) for values in difficulty_mistakes.values()]

    plt.figure()
    plt.bar(difficulties, avg_mistakes, color='skyblue')
    plt.title('Average Mistakes by Difficulty')
    plt.xlabel('Difficulty Level')
    plt.ylabel('Average Mistakes')
    plt.show()

# 3️⃣ Win/Loss — Pie Chart
def generate_win_loss_pie_chart(data):
    outcomes = Counter(row['Win'] for row in data)
    labels = outcomes.keys()
    sizes = outcomes.values()

    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['lightgreen', 'salmon'])
    plt.title('Win vs. Loss Distribution')
    plt.axis('equal')
    plt.show()

# 4️⃣ Hints Used — Pie Chart
def generate_hints_usage_pie_chart(data):
    hints_used = sum(1 for row in data if int(row['Hints Used']) > 0)
    no_hints_used = len(data) - hints_used

    plt.figure()
    plt.pie([hints_used, no_hints_used], labels=['Hints Used', 'No Hints'], autopct='%1.1f%%', startangle=140, colors=['gold', 'lightgrey'])
    plt.title('Hint Usage Distribution')
    plt.axis('equal')
    plt.show()

# 5️⃣ Time Played per Difficulty — Boxplot
def generate_time_per_difficulty_boxplot(data):
    times_by_difficulty = defaultdict(list)
    for row in data:
        times_by_difficulty[row['Difficulty']].append(time_to_seconds(row['Time']))

    difficulties = list(times_by_difficulty.keys())
    times = [times_by_difficulty[diff] for diff in difficulties]

    plt.figure()
    plt.boxplot(times, labels=difficulties)
    plt.title('Completion Time by Difficulty')
    plt.xlabel('Difficulty Level')
    plt.ylabel('Time (seconds)')
    plt.show()

# 6️⃣ Time vs. Mistakes — Scatter Plot
def generate_time_vs_mistakes_scatter(data):
    times = [time_to_seconds(row['Time']) for row in data]
    mistakes = [int(row['Mistakes']) for row in data]

    plt.figure()
    plt.scatter(times, mistakes, color='purple')
    plt.title('Time vs Mistakes')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Mistake Count')
    plt.grid(True)
    plt.show()