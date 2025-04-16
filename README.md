# DOKU+ - V0.5

**DOKU+** is an interactive, user-personalized Sudoku game built with Python and Pygame. It features a clean UI, account system, sound effects, difficulty levels, and progress tracking with points and levels.

---

## 📁 Folder Structure

doku_plus/
│
├── assets/
│   ├── avatars/              # User avatar images
│   │   ├── beer.png
│   │   ├── black_dog.png
│   │   ├── chick.png
│   │   ├── gorilla.png
│   │   ├── meerkat.png
│   │   ├── penguin.png
│   │   ├── rabbit.png
│   │   └── seal.png
│   ├── fonts/                # Custom fonts
│   │   ├── nunito.ttf
│   │   ├── nunito_bold.ttf
│   │   ├── nunito_bold_italic.ttf
│   │   └── nunito_italic.ttf
│   └── sounds/               # Game sound effects
│       ├── click.mp3
│       ├── exit.mp3
│       ├── hint.mp3
│       └── level_up.mp3
│
├── core/                     # Core logic and UI
│   ├── AuthScreen.py
│   ├── Menu.py
│   ├── SudokuBoard.py
│   ├── SudokuGame.py
│   ├── SudokuRenderer.py
│   ├── Timer.py
│   ├── UserManager.py
│   └── constants.py
│
├── data/                     # Save files and user data
│   ├── game_stats.csv
│   └── users.json
│
├── features/                 # Additional features
│   ├── analytics/
│   ├── Leaderboard.py
│   ├── PointTracker.py
│   ├── StatsTracker.py
│   └── Themes.py
│
├── .gitignore
├── README.md
├── main.py
└── requirements.txt
---

## 🔑 Features Implemented (V0.5)

- ✅ Login and Account System with Avatar Selection
- ✅ Four Difficulty Modes (Easy → Advanced)
- ✅ Sudoku puzzle generator and solver
- ✅ Point and Level System (100 points per level)
- ✅ Save per-user progress (JSON)
- ✅ Game HUD with timer, score, and mistakes
- ✅ "Game Paused" overlay with resume
- ✅ "Game Over" overlay with stats summary
- ✅ Hint System (track hint-filled cells)
- ✅ Background music and sound effects
- ✅ Clean and scalable UI design

---

## 🧠 Game Logic

- Validity checks for Sudoku moves
- Auto-solving with backtracking for puzzle generation
- Dynamic hint system shows correct number for random empty cell
- Points are only awarded for manual correct inputs
- Level up occurs every 100 points, extra points roll over
- Real-time stat tracking in CSV

---

## 🛠️ Technologies Used

- Python 3.12+
- Pygame
- CSV & JSON for data management

---

## 📦 Requirements

Install dependencies using pip:

```bash
pip install -r requirements.txt}

---

## 🚀 How to Run
python main.py

---

## 📌 Version
DOKU+ – V0.5

