# DOKU+ - V0.5

**DOKU+** is an interactive, user-personalized Sudoku game built with Python and Pygame. It features a clean UI, account system, sound effects, difficulty levels, and progress tracking with points and levels.

---

## 📁 Folder Structure

```bash
doku_plus/
│
├── assets/
│   ├── avatars/             # Avatar images (e.g. penguin, chick, etc.)
│   ├── fonts/               # Nunito font files used in game UI
│   └── sounds/              # Sound effects for UI (click, exit, hint, level-up)
│
├── core/
│   ├── AuthScreen.py        # Handles login and account creation UI
│   ├── Menu.py              # Main menu and difficulty selection
│   ├── SudokuBoard.py       # Sudoku puzzle generation, validation, solving
│   ├── SudokuGame.py        # Manages game logic, state, and hint system
│   ├── SudokuRenderer.py    # Drawing logic for game screen and overlays
│   ├── Timer.py             # In-game timer and pause/resume
│   ├── UserManager.py       # JSON-based user storage, authentication
│   └── constants.py         # Global colors, fonts, screen settings
│
├── data/
│   ├── game_stats.csv       # Game result logs (CSV)
│   └── users.json           # Stores user accounts, levels, and points
│
├── features/
│   ├── analytics/
│   │   └── Leaderboard.py   # (Future) Track and rank top users
│   ├── PointTracker.py      # Track and manage user score & level
│   ├── StatsTracker.py      # CSV logging of gameplay stats
│   └── Themes.py            # (Future) Switch between different UI themes
│
├── main.py                 # Main game controller loop
├── requirements.txt        # Python packages required
└── README.md               # This file
```

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
```
---

## 🚀 How to Run

```bash
python main.py
```
---

## 📌 Version
DOKU+ – V0.5
---

## 🙌 Author
Napat Kulnarong
---
