# PySudoku Solver - Utility Functions
# -----------------------------------
# Contains shared utility functions for parsing, formatting, and handling Sudoku puzzles.
# Used by both the command-line interface and the GUI.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

from typing import List

def parse_puzzle_string(puzzle_str: str) -> List[List[int]]:
    """
    Parses a string of 81 characters into a 9x9 Sudoku grid.
    Accepts '0', '.', 'x', or 'X' as unknowns, '1'-'9' as knowns.
    Raises ValueError if the string is not valid.
    """
    puzzle_str = puzzle_str.strip().replace('\n', '')
    if len(puzzle_str) != 81:
        raise ValueError("Puzzle string must be exactly 81 characters.")
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            c = puzzle_str[i * 9 + j]
            if c in '0.xX':
                row.append(0)
            elif c in '123456789':
                row.append(int(c))
            else:
                raise ValueError(f"Invalid character '{c}' in puzzle string.")
        grid.append(row)
    return grid

def puzzle_grid_to_string(grid: List[List[int]]) -> str:
    """
    Converts a 9x9 Sudoku grid to a string of 81 characters (0 for empty).
    """
    chars = []
    for i in range(9):
        for j in range(9):
            val = grid[i][j]
            chars.append(str(val) if val in range(1, 10) else "0")
    return ''.join(chars)

def get_puzzle_string_from_cells(cells) -> str:
    """
    Given a 9x9 list of QLineEdit cells, returns a string of 81 chars (0 for empty).
    """
    chars = []
    for row in cells:
        for cell in row:
            val = cell.text().strip()
            # Always append "0" if the cell is empty or not a digit 1-9
            chars.append("0" if not val or val not in "123456789" else val)
    return ''.join(chars)
