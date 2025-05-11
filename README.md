# DOKU+ - Your Personalized and Insightful Sudoku Experience

**DOKU+** is a sophisticated Sudoku game meticulously developed using Python and the Pygame library. It offers a rich and engaging experience with personalized user accounts, adaptive difficulty levels, intelligent in-game assistance, comprehensive tracking of your progress, and insightful visualizations of your gameplay statistics.

---

## 📂 Project Structure

```bash
doku_plus/
├── assets/
│   ├── avatars/          # User avatar images for profile personalization (bear.png, black_dog.png, ...)
│   ├── fonts/            # Nunito font files for a clean and consistent UI (nunito.ttf, nunito_bold.ttf, ...)
│   └── sounds/           # Engaging audio effects for user interactions and feedback (click.mp3, exit.mp3, ...)
│
├── core/
│   ├── pycache/      # Python bytecode cache directory
│   ├── AuthScreen.py     # Manages secure user authentication (login and registration)
│   ├── constants.py      # Defines global constants such as colors, fonts, and screen dimensions for consistent styling
│   ├── GameStatsScreen.py # Implements the screen for displaying detailed game statistics with graphs
│   ├── HowToPlay.py      # Offers an interactive guide for new players
│   ├── Leaderboard.py    # Displays player rankings based on skill and progress
│   ├── Menu.py           # Implements intuitive navigation through the game's main options
│   ├── PlayScreen.py     # Allows users to select their desired game difficulty
│   ├── SudokuBoard.py    # Handles the generation of diverse Sudoku puzzles and their validation
│   ├── SudokuGame.py     # Orchestrates the core game logic, state management, and hint system
│   ├── SudokuRenderer.py # Responsible for efficiently rendering the game board and UI elements
│   ├── Timer.py          # Implements accurate in-game time tracking with pause and resume
│   └── UserManager.py    # Manages persistent user data storage and retrieval using JSON
│
├── data/
│   ├── game_stats.csv    # Logs detailed gameplay statistics in a structured CSV format for analysis
│   └── users.json        # Stores user account information and their progress (levels, points)
│
├── features/
│   ├── pycache/      # Python bytecode cache directory
│   ├── analytics/
│   │   ├── pycache/  # Python bytecode cache directory
│   │   ├── dashboard.py  # Provides a visual overview of the user's game statistics and progress
│   │   └── graph_generator.py # Generates visual representations of gameplay statistics
│   ├── PointTracker.py   # Manages the accumulation and progression of user points and levels
│   └── StatsTracker.py   # Handles the logging of comprehensive gameplay statistics
│
├── main.py               # The primary script to launch the DOKU+ application
├── requirements.txt      # Lists the Python package dependencies for the project
└── README.md             # This comprehensive project documentation file
```

---

## ✨ Key Features

-   **Secure User Accounts:** Create and log into personalized accounts with avatar selection to track your individual progress and preferences.
-   **Adaptive Difficulty Levels:** Choose from four distinct difficulty modes (Easy, Medium, Hard, Advanced) that dynamically adjust the challenge to your skill.
-   **Intelligent Sudoku Engine:** Experience a continuous stream of uniquely generated and solvable Sudoku puzzles.
-   **Intuitive User Interface:** A clean and responsive Pygame-based interface ensures a seamless and enjoyable gaming experience.
-   **Real-time Game Tracking:** Monitor your gameplay with an integrated timer, score, and mistake counter.
-   **Progressive Point and Level System:** Earn points for correct moves and advance through levels, providing a sense of accomplishment and continuous motivation.
-   **Persistent User Data:** Your account information and game progress are securely saved, allowing you to resume your journey at any time.
-   **Insightful Game Statistics:** Access detailed statistics on your gameplay, including time played, accuracy, and hint usage, presented both numerically and visually through generated graphs.
-   **Helpful Hint System:** Utilize the intelligent hint system to get guidance without fully solving the puzzle, learning and improving your skills.
-   **Error Highlighting:** The game provides visual feedback on incorrect entries, aiding in learning and preventing mistakes.
-   **Pause and Resume:** Easily pause and resume your game without losing your current state.
-   **Interactive "How to Play" Guide:** New players can quickly learn the rules and strategies of Sudoku through an integrated tutorial.
-   **Immersive Sound Effects:** Carefully selected sound effects enhance user interactions and provide feedback.
-   **Leaderboard System:** Compete with other players and see how your skills rank on the global leaderboard.
-   **Visualized Analytics Dashboard:** A dedicated dashboard provides a clear overview of your key game statistics and progress through informative graphs.

---

## 🧠 Under the Hood: Game Mechanics and Design

-   **Robust Puzzle Generation:** The `SudokuBoard.py` module employs sophisticated algorithms to generate solvable Sudoku puzzles across all difficulty levels.
-   **Intelligent Input Validation:** The game rigorously validates user inputs against Sudoku rules, providing immediate feedback.
-   **Strategic Hint Implementation:** The hint system in `SudokuGame.py` is designed to offer guidance without trivializing the puzzle, promoting learning and strategic thinking.
-   **Merit-Based Scoring:** The `PointTracker.py` ensures that points are awarded for accurate manual entries, encouraging active problem-solving.
-   **Comprehensive Statistics Tracking:** The `StatsTracker.py` diligently records various gameplay metrics, providing a rich dataset for analysis and visualization.
-   **Data Persistence:** The `UserManager.py` utilizes JSON to efficiently store and retrieve user account data and progress.
-   **Visual Data Representation:** The `graph_generator.py` leverages libraries like Matplotlib (as indicated in `requirements.txt`) to create insightful visualizations of gameplay statistics, accessible through the `dashboard.py` and `GameStatsScreen.py`.
-   **Modular UI Design:** The game's UI is thoughtfully structured across modules like `AuthScreen.py`, `Menu.py`, `PlayScreen.py`, `GameStatsScreen.py`, and `HowToPlay.py` for maintainability and scalability.

---

## 🛠️ Core Technologies

-   **Python 3.12+:** The foundational programming language, chosen for its versatility and extensive libraries.
-   **Pygame 2.6.0:** A powerful and user-friendly Python library for multimedia and game development, handling graphics, input, and sound.
-   **Matplotlib 3.10.1:** A comprehensive library for creating static, interactive, and animated visualizations in Python, used for generating game statistics graphs.
-   **NumPy 2.2.4:** A fundamental package for numerical computation in Python, likely used for efficient data manipulation in puzzle generation and analysis.
-   **JSON:** For structured storage and retrieval of user account data and game progress.
-   **CSV:** For logging detailed gameplay statistics in a readily accessible format.

---

## 📦 Installation Guide

1.  Ensure you have Python 3.12 or a later version installed on your system.
2.  Install the necessary Python dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Getting Started

1.  Navigate to the project directory in your terminal.
2.  Execute the main script to launch DOKU+:

    ```bash
    python main.py
    ```

---

## 📂 File Descriptions

-   `assets/`: Contains all multimedia assets such as images, fonts, and sound effects.
-   `core/`: Houses the fundamental game logic and data management components.
    -   `AuthScreen.py`: Manages user authentication processes.
    -   `Menu.py`: Implements the main game menu and navigation.
    -   `SudokuBoard.py`: Handles Sudoku puzzle creation and validation.
    -   `SudokuGame.py`: Contains the core game state and logic.
    -   `SudokuRenderer.py`: Manages the rendering of the game interface.
    -   `Timer.py`: Implements the in-game timer functionality.
    -   `UserManager.py`: Handles user data storage and retrieval.
    -   `constants.py`: Defines global project-wide constants.
-   `data/`: Stores persistent game data, including user accounts and statistics.
    -   `game_stats.csv`: Stores detailed records of game sessions.
    -   `users.json`: Contains user account information and progress.
-   `features/`: Includes modules that add specific functionalities to the game.
    -   `analytics/`: Contains modules for game analysis and reporting.
        -   `Leaderboard.py`: Manages and displays player rankings.
        -   `graph_generator.py`: Creates visualizations of game statistics.
    -   `PointTracker.py`: Manages user score and level progression.
    -   `StatsTracker.py`: Handles the logging of gameplay statistics.
    -   `Themes.py`: (Future) For implementing UI theme customization.
-   `ui/`: Contains modules responsible for the user interface elements and screens.
    -   `dashboard.py`: Implements the user statistics dashboard.
    -   `GameStatsScreen.py`: Displays detailed game statistics with graphs.
    -   `HowToPlay.py`: Provides instructions on how to play the game.
    -   `PlayScreen.py`: Allows users to select the game difficulty.
    -   `screens/`: (Potentially contains other UI-related modules).
-   `main.py`: The entry point for running the DOKU+ application.
-   `requirements.txt`: Lists the external Python libraries required for the project.
-   `README.md`: This documentation file providing an overview of the project.

---

## 📌 Version Information

**DOKU+ - Version 0.5**

---

## 🧑‍💻 Developed By

Napat Kulnarong (6710545580)
