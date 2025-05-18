# PySudoku Solver
# ----------------
# A command-line Sudoku puzzle solver that reads puzzles from a text file, applies logic-based techniques and backtracking,
# and prints the solved puzzles in a formatted grid. Designed for extensibility and future UI integration.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

from typing import List, Optional, Tuple

def check_puzzle_solved(puzzle: List[List[int]]) -> bool:
    """
    Returns True if the puzzle is completely filled (no zeros remain).
    :param puzzle: 9x9 Sudoku grid
    :return: bool
    """
    return all(puzzle[row][col] != 0 for row in range(9) for col in range(9))

def is_possible(puzzle: List[List[int]], x: int, y: int, num: int) -> bool:
    """
    Checks if a number can be placed at position (x, y) without violating Sudoku rules.
    :param puzzle: 9x9 Sudoku grid
    :param x: Row index
    :param y: Column index
    :param num: Number to check (1-9)
    :return: bool
    """
    if puzzle[x][y] != 0:
        return False
    if any(puzzle[x][col] == num for col in range(9)):
        return False
    if any(puzzle[row][y] == num for row in range(9)):
        return False
    x0, y0 = (x // 3) * 3, (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if puzzle[x0 + i][y0 + j] == num:
                return False
    return True

def row_col_square_single_algo(puzzle: List[List[int]], puzzle_pos: List[List[list]]) -> bool:
    """
    Fills in cells that have only one possible value based on current puzzle state.
    Updates puzzle_pos with possible values for each cell.
    :param puzzle: 9x9 Sudoku grid
    :param puzzle_pos: 9x9 grid of possible values for each cell
    :return: True if a cell was filled, False otherwise
    """
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] != 0:
                puzzle_pos[row][col] = []
                continue
            possible_nums = [num for num in range(1, 10) if is_possible(puzzle, row, col, num)]
            if len(possible_nums) == 1:
                puzzle[row][col] = possible_nums[0]
                return True
            puzzle_pos[row][col] = possible_nums
    return False

def row_col_square_only_algo(puzzle: List[List[int]], puzzle_pos: List[List[list]]) -> bool:
    """
    Fills in cells where a number can only go in one place in a row, column, or 3x3 square.
    :param puzzle: 9x9 Sudoku grid
    :param puzzle_pos: 9x9 grid of possible values for each cell
    :return: True if a cell was filled, False otherwise
    """
    # Row
    for row in range(9):
        for num in range(1, 10):
            positions = [(row, col) for col in range(9) if num in puzzle_pos[row][col]]
            if len(positions) == 1:
                puzzle[positions[0][0]][positions[0][1]] = num
                return True
    # Column
    for col in range(9):
        for num in range(1, 10):
            positions = [(row, col) for row in range(9) if num in puzzle_pos[row][col]]
            if len(positions) == 1:
                puzzle[positions[0][0]][positions[0][1]] = num
                return True
    # Square
    for x in (0, 3, 6):
        for y in (0, 3, 6):
            for num in range(1, 10):
                positions = []
                for i in range(3):
                    for j in range(3):
                        row, col = x + i, y + j
                        if num in puzzle_pos[row][col]:
                            positions.append((row, col))
                if len(positions) == 1:
                    puzzle[positions[0][0]][positions[0][1]] = num
                    return True
    return False

def find_empty(puzzle: List[List[int]]) -> Optional[Tuple[int, int]]:
    """
    Finds the next empty cell (with value 0) in the puzzle.
    :param puzzle: 9x9 Sudoku grid
    :return: Tuple of (row, col) if found, else None
    """
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return (i, j)
    return None

def backtracking(puzzle: List[List[int]]) -> bool:
    """
    Solves the puzzle using recursive backtracking if logic-based methods fail.
    :param puzzle: 9x9 Sudoku grid
    :return: True if solved, False otherwise
    """
    empty = find_empty(puzzle)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_possible(puzzle, row, col, num):
            puzzle[row][col] = num
            if backtracking(puzzle):
                return True
            puzzle[row][col] = 0
    return False

def solve_puzzle(puzzle: List[List[int]], puzzle_pos: List[List[list]]) -> bool:
    """
    Attempts to solve the puzzle using logic-based algorithms first, then backtracking if needed.
    :param puzzle: 9x9 Sudoku grid
    :param puzzle_pos: 9x9 grid of possible values for each cell
    :return: True if solved, False otherwise
    """
    while True:
        if row_col_square_single_algo(puzzle, puzzle_pos):
            continue
        if row_col_square_only_algo(puzzle, puzzle_pos):
            continue
        break
    if check_puzzle_solved(puzzle):
        return True
    return backtracking(puzzle)

def print_puzzle(puzzle: List[List[int]]):
    """
    Prints the Sudoku puzzle in a formatted grid, matching the output format in the README.
    :param puzzle: 9x9 Sudoku grid
    """
    for row in range(9):
        if row % 3 == 0:
            print('------------------------')
        for col in range(9):
            if col == 0:
                print('|', end="")
            if col % 3 == 0 and col != 0:
                print('| ', end="")
            print(f"{puzzle[row][col]} ", end="")
        print('|')

def print_minimal_puzzle(puzzle: List[List[int]]):
    """
    Prints the puzzle as a single string of digits per row (minimal format).
    :param puzzle: 9x9 Sudoku grid
    """
    for row in puzzle:
        print(''.join(str(num) for num in row))

def load_puzzles_from_file(filename: str):
    """
    Loads puzzles from a text file in the expected format.
    :param filename: Path to the puzzle file
    :return: List of (puzzle_name, puzzle_grid) tuples
    """
    with open(filename, "r") as puzzle_file:
        puzzles = []
        puzzle = []
        puzzle_name = ''
        for line in puzzle_file:
            if 'Grid' in line:
                if puzzle:
                    puzzles.append((puzzle_name, puzzle))
                    puzzle = []
                puzzle_name = line.strip()
            else:
                row = [int(num) for num in line.strip() if num.isdigit()]
                if row:
                    puzzle.append(row)
        if puzzle:
            puzzles.append((puzzle_name, puzzle))
    return puzzles

def main():
    """
    Main entry point: loads puzzles, solves them, and prints results.
    """
    failed_count = 0
    puzzles = load_puzzles_from_file("puzzles/puzzles.txt")
    for puzzle_name, puzzle in puzzles:
        puzzle_pos = [[[] for _ in range(9)] for _ in range(9)]
        print(puzzle_name)
        solved = solve_puzzle(puzzle, puzzle_pos)
        if not solved:
            failed_count += 1
            print('Failed!')
        else:
            print_puzzle(puzzle)
            print('Success!')
    print(f"Failed {failed_count}")

if __name__ == '__main__':
    main()