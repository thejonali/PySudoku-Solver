# PySudoku Solver - Command Line Interface
# ----------------------------------------
# A command-line Sudoku puzzle solver that can solve puzzles from a text file or from a string passed as an argument.
# Uses logic-based techniques and backtracking, with solving logic separated into algorithms.py for modularity.
# Prints solved puzzles in a formatted grid. Designed for extensibility and future UI integration.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

import sys
from algorithms import (
    solve_puzzle,
    print_puzzle,
    load_puzzles_from_file,
)
from functions import parse_puzzle_string
from puzzle import SudokuPuzzle

def solve_puzzle_obj(puzzle_obj: SudokuPuzzle):
    """
    Solves a SudokuPuzzle object and returns the solved grid (list of lists) or None if failed.
    """
    from algorithms import solve_puzzle
    grid = puzzle_obj.get_grid()
    puzzle_pos = [[[] for _ in range(9)] for _ in range(9)]
    solved = solve_puzzle(grid, puzzle_pos)
    if solved:
        puzzle_obj.set_grid(grid)
        return grid
    return None

def solve(puzzle_str: str):
    """
    Solves a puzzle from a string of 81 chars and returns the solved grid (list of lists) or None if failed.
    """
    puzzle = SudokuPuzzle()
    puzzle.set_from_string(puzzle_str)
    return solve_puzzle_obj(puzzle)

def main():
    """
    Main entry point: solves a puzzle from a string of 81 characters or from a file.
    Prints usage instructions if no argument is provided.
    """
    if len(sys.argv) <= 1:
        print(
            "Please provide an 81 character string (digits 1-9, 0, ., x, or X for blanks),\n"
            "or provide the location of a file containing puzzle(s).\n"
            "Examples:\n"
            "  python solver.py 530070000600195000098000060800060003400803001700020006060000280000419005000080079\n"
            "  python solver.py puzzles/puzzles.txt"
        )
        return

    arg = sys.argv[1].strip()
    is_file = (
        '.' in arg and len(arg.split('.')[-1]) > 0 and
        not (len(arg) == 81 and all(c in '1234567890.xX' for c in arg))
    )
    if is_file:
        filename = arg
        failed_count = 0
        puzzles = load_puzzles_from_file(filename)
        for puzzle_name, puzzle_grid in puzzles:
            puzzle_obj = SudokuPuzzle()
            puzzle_obj.set_grid(puzzle_grid)
            solved_grid = solve_puzzle_obj(puzzle_obj)
            print(puzzle_name)
            if not solved_grid:
                failed_count += 1
                print('Failed!')
            else:
                print_puzzle(solved_grid)
                print('Success!')
        print(f"Failed {failed_count}")
    else:
        puzzle_str = arg.replace('\n', '')
        if len(puzzle_str) != 81 or not all(c in '1234567890.xX' for c in puzzle_str):
            print('Input must be a string of exactly 81 characters (digits 1-9, 0, ., x, or X for blanks).')
            return
        puzzle_obj = SudokuPuzzle()
        puzzle_obj.set_from_string(puzzle_str)
        solved_grid = solve_puzzle_obj(puzzle_obj)
        if not solved_grid:
            print('Failed!')
        else:
            print_puzzle(solved_grid)
            print('Success!')

if __name__ == '__main__':
    main()