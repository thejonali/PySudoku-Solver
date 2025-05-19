from typing import List, Optional, Tuple, Any

class PuzzleBase:
    """
    Abstract base class for a Sudoku puzzle.
    """
    def get_grid(self) -> List[List[int]]:
        raise NotImplementedError

    def set_grid(self, grid: List[List[int]]) -> None:
        raise NotImplementedError

    def set_from_string(self, puzzle_str: str) -> None:
        raise NotImplementedError

    def set_from_file(self, filename: str) -> None:
        raise NotImplementedError

    def to_string(self) -> str:
        raise NotImplementedError

class SudokuPuzzle(PuzzleBase):
    """
    Concrete implementation of a 9x9 Sudoku puzzle.
    """
    def __init__(self, grid: Optional[List[List[int]]] = None):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        if grid:
            self.set_grid(grid)

    def get_grid(self) -> List[List[int]]:
        """
        Returns the current puzzle grid.
        """
        return [row[:] for row in self.grid]

    def set_grid(self, grid: List[List[int]]) -> None:
        """
        Sets the puzzle grid.
        """
        if len(grid) != 9 or any(len(row) != 9 for row in grid):
            raise ValueError("Grid must be 9x9.")
        self.grid = [row[:] for row in grid]

    def set_from_string(self, puzzle_str: str) -> None:
        """
        Sets the puzzle grid from a string of 81 characters.
        Accepts 0, ., x, X as blanks.
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
        self.set_grid(grid)

    def set_from_file(self, filename: str) -> None:
        """
        Loads the first puzzle from a file and sets the grid.
        """
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        # Try to find the first 9 lines of digits
        puzzle_lines = []
        for line in lines:
            digits = [int(c) if c in "123456789" else 0 for c in line if c in "1234567890.xX"]
            if len(digits) == 9:
                puzzle_lines.append(digits)
            if len(puzzle_lines) == 9:
                break
        if len(puzzle_lines) != 9:
            raise ValueError("Could not find a valid 9x9 puzzle in file.")
        self.set_grid(puzzle_lines)

    def to_string(self) -> str:
        """
        Returns the puzzle as a string of 81 characters (0 for blanks).
        """
        return ''.join(str(self.grid[i][j]) if self.grid[i][j] != 0 else '0'
                       for i in range(9) for j in range(9))
