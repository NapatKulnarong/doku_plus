import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
matplotlib.use('Agg')

# Set up paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRAPHS_DIR = os.path.join(BASE_DIR, "assets", "stats_graphs")
os.makedirs(GRAPHS_DIR, exist_ok=True)


def _save_figure(filename):
    """Helper function to save figures consistently"""
    path = os.path.join(GRAPHS_DIR, filename)
    plt.savefig(path, bbox_inches='tight', dpi=100)
    plt.close()
    return path


def convert_time_to_seconds(time_str):
    """Converts time in 'MM:SS' format to total seconds."""
    try:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    except:
        return 0


def generate_time_played_line_graph(data):
    """Generates a line graph for average time played per session by difficulty."""
    df = pd.DataFrame(data)
    df['Time Played'] = df['Time'].apply(convert_time_to_seconds)
    df['Date'] = pd.to_datetime(df['Timestamp']).dt.date

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='Date', y='Time Played', hue='Difficulty',
                 palette='viridis', marker='o')
    plt.title('Time Played Over Time by Difficulty')
    plt.xlabel('Date')
    plt.ylabel('Time Played (seconds)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    _save_figure('time_played_line.png')


def generate_mistakes_bar_chart(data):
    """Generates a bar chart of average mistakes by difficulty."""
    df = pd.DataFrame(data)
    df['Mistakes'] = pd.to_numeric(df['Mistakes'])

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x='Difficulty', y='Mistakes', errorbar=None,
                     hue='Difficulty', palette=['#4CAF50', '#FFC107', '#FF9800', '#F44336'],
                     legend=False)

    # Add value labels
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10),
                    textcoords='offset points', fontweight='bold')

    plt.title('Average Mistakes by Difficulty', fontsize=14, pad=20)
    plt.xlabel('Difficulty Level', fontweight='bold')
    plt.ylabel('Average Mistakes', fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    _save_figure('mistakes_bar.png')


def generate_win_loss_pie_chart(data):
    """Generates a pie chart of win/loss distribution."""
    df = pd.DataFrame(data)
    win_counts = df['Win'].value_counts()

    plt.figure(figsize=(8, 8))
    patches, texts, autotexts = plt.pie(
        win_counts,
        labels=['Wins', 'Losses'],
        colors=['#66BB6A', '#EF5350'],
        explode=(0.05, 0),
        autopct='%1.1f%%',
        startangle=140,
        shadow=True,
        textprops={'fontsize': 12, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'black', 'linewidth': 1}
    )

    for autotext in autotexts:
        autotext.set_color('white')

    plt.title(f'Win/Loss Distribution\n({win_counts["Win"]} Wins vs {win_counts.get("Loss", 0)} Losses)',
              fontsize=14, pad=20)
    plt.axis('equal')
    _save_figure('win_loss_pie.png')


def generate_hints_usage_pie_chart(data):
    """Generates a pie chart of hint usage."""
    df = pd.DataFrame(data)
    df['Hints Used'] = pd.to_numeric(df['Hints Used'])
    usage = ['Used Hints' if x > 0 else 'No Hints' for x in df['Hints Used']]
    usage_counts = pd.Series(usage).value_counts()

    plt.figure(figsize=(8, 8))
    patches, texts, autotexts = plt.pie(
        usage_counts,
        labels=usage_counts.index,
        colors=['#FFD700', '#E0E0E0'],
        explode=(0.05, 0),
        autopct=lambda p: f'{p:.1f}%\n({int(p / 100 * len(data))})',
        startangle=140,
        shadow=True,
        textprops={'fontsize': 11, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'black', 'linewidth': 1}
    )

    plt.title(f'Hint Usage Distribution\nTotal Games: {len(data)}', fontsize=14, pad=20)
    plt.axis('equal')
    _save_figure('hints_pie.png')


def generate_time_per_difficulty_boxplot(data):
    """Generates a boxplot of time played by difficulty."""
    df = pd.DataFrame(data)
    df['Time Played'] = df['Time'].apply(convert_time_to_seconds)

    plt.figure(figsize=(12, 7))
    ax = sns.boxplot(data=df, x='Difficulty', y='Time Played',
                     hue='Difficulty', palette=['#2ecc71', '#f39c12', '#e74c3c', '#9b59b6'],
                     legend=False)

    # Create custom y-axis labels
    secs = np.linspace(ax.get_ylim()[0], ax.get_ylim()[1], num=5)
    mins = secs // 60
    remaining_secs = secs % 60
    y_labels = [f"{int(m)}:{int(s):02d}" for m, s in zip(mins, remaining_secs)]
    ax.set_yticks(secs)
    ax.set_yticklabels(y_labels)

    plt.title('Completion Time Distribution by Difficulty', fontsize=14, pad=20)
    plt.xlabel('Difficulty Level', fontweight='bold')
    plt.ylabel('Completion Time (min:sec)', fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    _save_figure('time_boxplot.png')


def generate_correlation_matrix(data):
    """Generates a correlation matrix heatmap."""
    df = pd.DataFrame(data)

    # Convert columns to numeric values
    df['Time'] = df['Time'].apply(convert_time_to_seconds)
    for col in ['Mistakes', 'Hints Used', 'Filled Cells']:
        df[col] = pd.to_numeric(df[col])

    # Add win as binary
    df['Win Binary'] = (df['Win'] == 'Win').astype(int)

    # Calculate correlation
    corr = df[['Time', 'Mistakes', 'Hints Used', 'Filled Cells', 'Win Binary']].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, vmin=-1, vmax=1,
                annot_kws={'fontweight': 'bold'})
    plt.title('Game Metrics Correlation Matrix', fontsize=14, pad=20)
    _save_figure('correlation_matrix.png')


def generate_time_statistics_table(data):
    """Generates a properly formatted table of time statistics grouped by difficulty in specific order."""
    df = pd.DataFrame(data)
    df['Time Played'] = df['Time'].apply(convert_time_to_seconds)

    # Define the correct difficulty order
    difficulty_order = ['easy', 'medium', 'hard', 'advanced']

    # Group by difficulty and calculate statistics
    grouped = df.groupby('Difficulty')['Time Played'].agg([
        ('n', 'count'),
        ('min', 'min'),
        ('max', 'max'),
        ('range', lambda x: x.max() - x.min()),
        ('mean', 'mean'),
        ('median', 'median'),
        ('stdev', 'std')
    ]).reset_index()

    # Ensure all difficulty levels are present and ordered correctly
    for diff in difficulty_order:
        if diff not in grouped['Difficulty'].values:
            grouped = grouped.append({
                'Difficulty': diff,
                'n': 0,
                'min': None,
                'max': None,
                'range': None,
                'mean': None,
                'median': None,
                'stdev': None
            }, ignore_index=True)

    # Convert Difficulty to ordered category for sorting
    grouped['Difficulty'] = pd.Categorical(
        grouped['Difficulty'],
        categories=difficulty_order,
        ordered=True
    )
    grouped = grouped.sort_values('Difficulty')

    # Format the statistics
    formatted_stats = grouped.copy()
    formatted_stats['n'] = formatted_stats['n'].astype(int).astype(str)
    for col in ['min', 'max', 'range', 'mean', 'median', 'stdev']:
        formatted_stats[col] = formatted_stats[col].apply(
            lambda x: f"{x:.1f}" if pd.notna(x) and x != 0 else "-"
        )

    # Capitalize difficulty names for display
    formatted_stats['Difficulty'] = formatted_stats['Difficulty'].str.capitalize()

    # Create the figure
    plt.figure(figsize=(10, 4))  # Wider figure to accommodate more columns
    ax = plt.gca()
    ax.axis('off')

    # Define colors
    header_color = '#3498db'
    row_colors = ['#f8f8f8', '#f0f0f0']  # Alternating row colors
    difficulty_color = '#2c3e50'

    # Create table with proper formatting
    table = ax.table(
        cellText=formatted_stats.iloc[:, 1:].values,  # Skip Difficulty column for cell text
        rowLabels=formatted_stats['Difficulty'],
        colLabels=['n', 'min', 'max', 'range', 'mean', 'median', 'stdev'],
        loc='center',
        cellLoc='center',
        colColours=[header_color] * 7,
        cellColours=[[row_colors[i % 2]] * 7 for i in range(len(formatted_stats))]
    )

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2)  # Adjusted scale for better fit

    # Customize cell appearance
    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor('#dddddd')
        cell.set_linewidth(0.5)
        if i == 0:  # Header row
            cell.set_text_props(color='white', fontweight='bold')
            cell.set_facecolor(header_color)
        else:  # Data cells
            cell.set_text_props(color='#333333')
            # Highlight difficulty column
            if j == -1:  # First column (row labels)
                cell.set_text_props(color='white', fontweight='bold')
                cell.set_facecolor(difficulty_color)

    plt.title('Time Played Statistics by Difficulty (seconds)', fontsize=12, pad=20)
    plt.tight_layout()
    _save_figure('time_stats_table.png')


def generate_all_graphs(data):
    """Generate and save all graphs"""
    try:
        generate_time_played_line_graph(data)
        generate_mistakes_bar_chart(data)
        generate_win_loss_pie_chart(data)
        generate_hints_usage_pie_chart(data)
        generate_time_per_difficulty_boxplot(data)
        generate_correlation_matrix(data)
        generate_time_statistics_table(data)
        return True
    except Exception as e:
        print(f"Error generating graphs: {e}")
        return False
