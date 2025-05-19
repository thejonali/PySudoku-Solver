# PySudoku Solver

A feature-rich Sudoku solver with both a command-line interface and a modern PyQt5 GUI. Supports logic-based solving, backtracking, puzzle loading from files, multiple color themes, and a built-in timer for puzzle solving.

---

## Features

- **Command-Line Solver**: Solve puzzles from strings or files.
- **PyQt5 GUI**: Interactive Sudoku board with timer, theming, and file loading.
- **Multiple Themes**: Choose from Panda, Ocean, Forest, and Sunset color schemes.
- **Timer**: Start, pause, resume, and see your solve time.
- **File Loading**: Load puzzles from text files via the GUI or CLI.
- **Polymorphic Puzzle Class**: All puzzle logic is encapsulated in a `SudokuPuzzle` class for extensibility and clean code.

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/thejonali/PySudoku-Solver.git
    cd PySudoku-Solver
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **(Optional) Docker:**
    ```bash
    docker build -t pysudoku .
    ```

---

## Usage

### Command-Line Interface

Solve a puzzle from a string (81 characters, use `0`, `.`, `x`, or `X` for blanks):

```bash
python solver.py 530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

Solve all puzzles in a file:

```bash
python solver.py puzzles/puzzles.txt
```

If no argument is provided, usage instructions will be printed.

#### Docker CLI Example

```bash
docker run --rm -it pysudoku python solver.py 530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

---

### Graphical User Interface (GUI)

Start the GUI:

```bash
python main.py
```

Optionally, prefill the board with a puzzle string:

```bash
python main.py 530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

#### Docker GUI Example

```bash
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix pysudoku python main.py
```

---

## GUI Features

- **Start/Pause/Resume Timer**: Click "Start" to begin timing your solve. The button toggles to "Pause" and "Resume".
- **Solve**: Automatically solves the current board and animates the solution.
- **Clear**: Clears the board and resets the timer.
- **Themes**: Change the board's color scheme from the "Themes" menu.
- **File > Load From File**: Load a puzzle from a text file (loads the first puzzle found).
- **Cells with initial numbers are locked when the timer starts.**

---

## Puzzle File Format

- Each puzzle should be 9 lines of 9 digits (0, ., x, X, or 1-9).
- Example:
    ```
    530070000
    600195000
    098000060
    800060003
    400803001
    700020006
    060000280
    000419005
    000080079
    ```

---

## Developer Notes

- All puzzle logic is encapsulated in `puzzle.py` (`SudokuPuzzle` class).
- Algorithms are in `algorithms.py`.
- Utility functions are in `functions.py`.
- The GUI is in `main.py`.
- The CLI is in `solver.py`.
- The project is designed for extensibility and clean separation of concerns.

---

## License

Apache 2.0

---

## Author

thejonali (https://github.com/thejonali)
