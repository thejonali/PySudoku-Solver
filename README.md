# PySudoku Solver

PySudoku Solver is a command-line Sudoku puzzle solver written in Python. It reads puzzles from a text file, solves them using logic-based techniques and backtracking, and prints the solutions in a readable format.

## Features
- Reads multiple Sudoku puzzles from a text file (see `puzzles/puzzles.txt`)
- Uses logic-based algorithms and backtracking to solve puzzles
- Prints solved puzzles in a formatted grid
- Reports failed attempts

## Usage
1. Place your Sudoku puzzles in `puzzles/puzzles.txt` (see the provided format).
2. Run the solver:
   ```sh
   python solver.py
   ```
3. The program will print each puzzle name, the solved grid, and whether it was solved successfully.

## Puzzle File Format
- Each puzzle starts with a line containing the word `Grid` (e.g., `Grid 01`)
- Each subsequent line contains 9 digits (0 for empty cells)
- Example:
  ```
  Grid 01
  003020600
  900305001
  001806400
  008102900
  700000008
  006708200
  002609500
  800203009
  005010300
  ```

## Puzzle Output Format
After solving, puzzles are displayed in the terminal as follows:

```
Grid 01
------------------------
|4 8 3 | 9 2 1 | 6 5 7 |
|9 6 7 | 3 4 5 | 8 2 1 |
|2 5 1 | 8 7 6 | 4 9 3 |
------------------------
|5 4 8 | 1 3 2 | 9 7 6 |
|7 2 9 | 5 6 4 | 1 3 8 |
|1 3 6 | 7 9 8 | 2 4 5 |
------------------------
|3 7 2 | 6 8 9 | 5 1 4 |
|8 1 4 | 2 5 3 | 7 6 9 |
|6 9 5 | 4 1 7 | 3 8 2 |
Success!
```

## Roadmap: Version 2 (Coming Soon!)
- **Graphical User Interface (UI):**
  - Import your own `.txt` puzzle files and see them displayed in the UI
  - Manually update a blank Sudoku grid and hit "Solve" to see the solution
  - Generate new puzzles for you to solve, with progress tracking and statistics

Stay tuned for updates and new features!

---

**Author:** [thejonali](https://github.com/thejonali)

**License:** Apache 2.0
