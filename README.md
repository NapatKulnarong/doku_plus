# DOKU+ - Your Personalized and Insightful Sudoku Experience

**DOKU+** is a sophisticated Sudoku game meticulously developed using Python and the Pygame library. It offers a rich and engaging experience with personalized user accounts, adaptive difficulty levels, intelligent in-game assistance, comprehensive tracking of your progress, and insightful visualizations of your gameplay statistics.

---

## 📂 Project Structure

```bash
doku_plus/
├── assets/
│   ├── avatars/               # User avatar images for profile personalization (bear.png, black_dog.png, ...)
│   ├── fonts/                 # Nunito font files for a clean and consistent UI (nunito.ttf, nunito_bold.ttf, ...)
│   └── sounds/                # Engaging audio effects for user interactions and feedback (click.mp3, exit.mp3, ...)
│
├── core/
│   ├── pycache/               # Python bytecode cache directory
│   ├── AuthScreen.py          # Manages secure user authentication (login and registration)
│   ├── constants.py           # Defines global constants such as colors, fonts, and screen dimensions for consistent styling
│   ├── GameStatsScreen.py     # Implements the screen for displaying detailed game statistics with graphs
│   ├── HowToPlay.py           # Offers an interactive guide for new players
│   ├── Leaderboard.py         # Displays player rankings based on skill and progress
│   ├── Menu.py                # Implements intuitive navigation through the game's main options
│   ├── PlayScreen.py          # Allows users to select their desired game difficulty
│   ├── SudokuBoard.py         # Handles the generation of diverse Sudoku puzzles and their validation
│   ├── SudokuGame.py          # Orchestrates the core game logic, state management, and hint system
│   ├── SudokuRenderer.py      # Responsible for efficiently rendering the game board and UI elements
│   ├── Timer.py               # Implements accurate in-game time tracking with pause and resume
│   └── UserManager.py         # Manages persistent user data storage and retrieval using JSON
│
├── data/
│   ├── game_stats.csv         # Logs detailed gameplay statistics in a structured CSV format for analysis
│   └── users.json             # Stores user account information and their progress (levels, points)
│
├── features/
│   ├── pycache/               # Python bytecode cache directory
│   ├── analytics/
│   │   ├── pycache/           # Python bytecode cache directory
│   │   ├── dashboard.py       # Provides a visual overview of the user's game statistics and progress
│   │   └── graph_generator.py # Generates visual representations of gameplay statistics
│   ├── PointTracker.py        # Manages the accumulation and progression of user points and levels
│   └── StatsTracker.py        # Handles the logging of comprehensive gameplay statistics
│
├── main.py                    # The primary script to launch the DOKU+ application
├── requirements.txt           # Lists the Python package dependencies for the project
└── README.md                  # This comprehensive project documentation file
```

---
---

## 📦 Installation Guide

To get DOKU+ running successfully on your system, please follow these detailed instructions:

1.  **Prerequisites:** Ensure that you have **Python 3.12 or a later version** installed. You can check your Python version by opening your terminal or command prompt and running:
    ```bash
    python --version
    ```
    If you do not have Python 3.12 or later installed, please download it from the official Python website ([https://www.python.org/downloads/](https://www.python.org/downloads/)) and follow the installation instructions for your operating system.

2.  **Install Dependencies:** DOKU+ relies on several external Python libraries. These dependencies are listed in the `requirements.txt` file. To install them, navigate to the root directory of the DOKU+ project in your terminal or command prompt and run the following command:
    ```bash
    pip install -r requirements.txt
    ```
    This command will automatically download and install all the necessary libraries, including Pygame, Matplotlib, and NumPy. Ensure that this process completes without any errors.

---

## 🚀 Getting Started

Once you have successfully installed the prerequisites and dependencies, you can launch the DOKU+ game by following these steps:

1.  **Navigate to the Project Directory:** Open your terminal or command prompt and navigate to the root directory of the DOKU+ project. This is the directory containing the `main.py` file.

2.  **Run the Game:** Execute the main script using the Python interpreter:
    ```bash
    python main.py
    ```
    Press the Enter key after typing this command. The DOKU+ game window should now open, and you can begin playing.

**Important Notes:**

* Ensure that you run the `pip install -r requirements.txt` command from the correct project directory, where the `requirements.txt` file is located.
* If you encounter any issues during the installation process, double-check that you have the correct version of Python installed and that your internet connection is stable for downloading the dependencies.
* The game should run smoothly on most modern operating systems (Windows, macOS, Linux) that support Python and Pygame.

---
