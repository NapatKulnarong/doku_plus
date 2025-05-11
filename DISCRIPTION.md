# DOKU+ - Your Personalized and Insightful Sudoku Experience

[![Project Overview](link_to_your_project_screenshot_or_gif_here)](link_to_your_project_demo_video_here)

**DOKU+** is a sophisticated and feature-rich Sudoku game meticulously developed using Python and the Pygame library. This project aims to elevate the classic Sudoku experience by providing users with personalized accounts, dynamically adaptive difficulty levels, intelligent in-game assistance, comprehensive tracking of their progress, and insightful visualizations of their gameplay statistics.

## ♥︎ Overview and Concept

DOKU+ offers a compelling blend of traditional Sudoku gameplay with modern user experience enhancements and data-driven insights. Players engage with the familiar 9x9 grid, striving to fill in numbers 1-9 such that each row, column, and 3x3 subgrid contains each digit exactly once. However, DOKU+ goes beyond the standard game by incorporating:

* **Personalized User Experience:** Players can create secure accounts, choose avatars, and track their individual progress through a point and leveling system.
* **Adaptive Difficulty:** Four distinct difficulty levels cater to players of all skill levels, ensuring a consistently engaging challenge.
* **Intelligent Assistance:** An integrated hint system provides guidance without solving the puzzle outright, promoting learning and strategic thinking.
* **Comprehensive Progress Tracking:** Detailed statistics on gameplay (time, mistakes, hints used) are recorded and visualized to provide players with insights into their performance.
* **Engaging User Interface:** A clean and intuitive Pygame-based interface ensures a smooth and enjoyable gaming experience across various screens (authentication, menu, gameplay, statistics, leaderboard, how-to-play).

The core concept behind DOKU+ is to provide not just a Sudoku game, but a personalized journey of improvement and engagement. By tracking progress, offering feedback through statistics, and providing intelligent assistance, DOKU+ aims to be both entertaining and a tool for enhancing logical thinking skills.

## 📜 UML Class Diagram
![DOKU+ UML Class Diagram](https://github.com/NapatKulnarong/doku_plus/blob/main/UML_Diagram.png)
---
## 🔑 Key Features
- Secure User Accounts: Login and registration with password hashing and avatar selection.
- Multiple Difficulty Levels: Easy, Medium, Hard, and Advanced.
- Dynamic Puzzle Generation: Solvable Sudoku puzzles created using a backtracking algorithm.
- Interactive Gameplay: Intuitive cell selection and number input.
- Real-time Timer: Tracks game duration.
- Point and Level System: Rewards correct moves and tracks long-term progress.
- Detailed Game Statistics: Logging and visualization of time, mistakes, and hints used.
- Intelligent Hint System: Provides guidance on correct cell values.
- Error Highlighting: Visual feedback for incorrect inputs.
- Pause and Resume Functionality: Allows players to interrupt and continue their games.
- How to Play Guide: Integrated instructions for new players.
- Leaderboard: Displays top players ranked by level and points.
- Visual Analytics Dashboard: Presents gameplay statistics through various graphs.
- Immersive Sound Effects: Enhances the user experience with audio feedback.
---
## 📡 Core Technologies
- Python 3.12+
- Pygame 2.6.0
- Matplotlib 3.10.1
- NumPy 2.2.4
- JSON for user data storage
- CSV for game statistics logging
---
## 🖥️ Installation
1. Ensure Python 3.12 or a later version is installed on your system.
2. Install the required Python packages:
```bash
pip install -r requirements.txt
```
---
## 🧑‍💻 Running the Game
1. Navigate to the project directory in your terminal.
2. Execute the main script:
```bash
python main.py
```
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
## Developed By
```
Napat Kulnarong (6710545580)
```
---
MIT License

Copyright (c) 2025 Napat Kulnarong

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

