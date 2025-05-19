# PySudoku Solver - Main Entry Point
# ----------------------------------
# Displays the PySudoku Solver title and provides a PyQt5 GUI for puzzle input and solving.
#
# Author: thejonali (https://github.com/thejonali)
# License: Apache 2.0

from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QAction, QFileDialog, QMessageBox, QActionGroup
)
from PyQt5.QtCore import Qt, QTimer
import sys
import solver
from puzzle import SudokuPuzzle

class SudokuUI(QWidget):
    """
    Main Sudoku GUI class. Handles grid display, user input, theming, file loading, and puzzle solving.
    """
    def __init__(self, puzzle_str=None):
        """
        Initialize the Sudoku UI. Optionally prefill the grid with a puzzle string.
        """
        super().__init__()
        self.setWindowTitle("PySudoku Solver")
        self.timer_running = False
        self.elapsed_seconds = 0
        self.theme = "Panda"
        self.puzzle = SudokuPuzzle()
        self.themes = {
            "Panda": {
                "white": "background: #eee; color: black;",
                "black": "background: #222; color: white;",
                "border": "1px solid #888"
            },
            "Ocean": {
                "white": "background: #b3e0ff; color: #00334d;",
                "black": "background: #005073; color: #b3e0ff;",
                "border": "1px solid #005073"
            },
            "Forest": {
                "white": "background: #e6ffe6; color: #003300;",
                "black": "background: #336633; color: #e6ffe6;",
                "border": "1px solid #336633"
            },
            "Sunset": {
                "white": "background: #fff0e6; color: #b34700;",
                "black": "background: #ff944d; color: #fff0e6;",
                "border": "1px solid #b34700"
            }
        }
        self.init_ui()
        if puzzle_str:
            self.set_puzzle_from_string(puzzle_str)

    def init_ui(self):
        """
        Set up the UI layout, menu bar, grid, and control buttons.
        """
        main_layout = QVBoxLayout()

        # --- Menu Bar ---
        self.menu_bar = QMenuBar(self)
        file_menu = QMenu("File", self)
        load_action = QAction("Load From File", self)
        load_action.triggered.connect(self.load_from_file)
        file_menu.addAction(load_action)
        self.menu_bar.addMenu(file_menu)

        # Theme menu (exclusive selection)
        theme_menu = QMenu("Themes", self)
        self.theme_actions = {}
        theme_action_group = QActionGroup(self)
        theme_action_group.setExclusive(True)
        for theme_name in self.themes:
            theme_action = QAction(theme_name, self)
            theme_action.setCheckable(True)
            theme_action.setActionGroup(theme_action_group)
            if theme_name == self.theme:
                theme_action.setChecked(True)
            # Use lambda with default arg to avoid late binding
            theme_action.triggered.connect(lambda checked, t=theme_name: self.set_theme(t))
            theme_menu.addAction(theme_action)
            self.theme_actions[theme_name] = theme_action
        self.menu_bar.addMenu(theme_menu)

        main_layout.setMenuBar(self.menu_bar)

        # --- Title ---
        title = QLabel("PySudoku Solver")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(title)

        # --- Timer ---
        self.timer_label = QLabel("Timer: 00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        main_layout.addWidget(self.timer_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # --- Sudoku Grid ---
        self.grid_layout = QGridLayout()
        self.cells = []
        for i in range(9):
            row_cells = []
            for j in range(9):
                cell = QLineEdit()
                cell.setFixedSize(32, 32)
                cell.setMaxLength(1)
                cell.setAlignment(Qt.AlignCenter)
                row_cells.append(cell)
                self.grid_layout.addWidget(cell, i, j)
            self.cells.append(row_cells)
        main_layout.addLayout(self.grid_layout)
        self.apply_theme(self.theme)

        # --- Control Buttons ---
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle_timer)
        btn_layout.addWidget(self.start_btn)

        solve_btn = QPushButton("Solve")
        solve_btn.clicked.connect(self.solve_puzzle)
        btn_layout.addWidget(solve_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_board)
        btn_layout.addWidget(clear_btn)

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.setFixedSize(self.sizeHint())

    def apply_theme(self, theme_name):
        """
        Apply the selected theme to the Sudoku grid.
        """
        theme = self.themes[theme_name]
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                # Each property must be separated by a semicolon, and border must be a valid CSS border property
                if ((i // 3 + j // 3) % 2 == 0):
                    style = f"font-size: 18px; border: {theme['border']}; {theme['white']}"
                else:
                    style = f"font-size: 18px; border: {theme['border']}; {theme['black']}"
                cell.setStyleSheet(style)

    def set_theme(self, theme_name):
        """
        Set the current theme and update the menu check state.
        """
        self.theme = theme_name
        self.apply_theme(theme_name)
        for name, action in self.theme_actions.items():
            action.setChecked(name == theme_name)

    def load_from_file(self):
        """
        Open a file dialog to select a puzzle file and load the first puzzle into the grid.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Puzzle File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                self.puzzle.set_from_file(file_path)
                self.clear_board()  # Also resets timer and unlocks cells
                self.set_puzzle_from_grid(self.puzzle.get_grid())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load puzzle: {e}")

    def toggle_timer(self):
        """
        Start, pause, or resume the timer.
        When starting, lock all cells that currently have numbers.
        """
        if not self.timer_running:
            self.timer.start(1000)
            self.timer_running = True
            self.start_btn.setText("Pause")
            for row in self.cells:
                for cell in row:
                    val = cell.text().strip()
                    if val and val in "123456789":
                        cell.setReadOnly(True)
                    else:
                        cell.setReadOnly(False)
        else:
            self.timer.stop()
            self.timer_running = False
            self.start_btn.setText("Resume")

    def update_timer(self):
        """
        Update the timer label every second.
        """
        self.elapsed_seconds += 1
        mins = self.elapsed_seconds // 60
        secs = self.elapsed_seconds % 60
        self.timer_label.setText(f"Timer: {mins:02d}:{secs:02d}")

    def clear_board(self):
        """
        Clears all cells in the grid and resets the window title and timer.
        Also unlocks all cells.
        """
        for row in self.cells:
            for cell in row:
                cell.clear()
                cell.setReadOnly(False)
        self.setWindowTitle("PySudoku Solver")
        self.timer.stop()
        self.timer_running = False
        self.elapsed_seconds = 0
        self.timer_label.setText("Timer: 00:00")
        self.start_btn.setText("Start")
        self.start_btn.setEnabled(True)

    def get_puzzle_string(self):
        """
        Returns the current grid as a string of 81 chars (0 for empty).
        Uses the puzzle object for consistency.
        """
        # Update puzzle object from UI before returning string
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[i][j].text().strip()
                if val and val in "123456789":
                    row.append(int(val))
                else:
                    row.append(0)
            grid.append(row)
        self.puzzle.set_grid(grid)
        return self.puzzle.to_string()

    def set_puzzle_from_grid(self, grid):
        """
        Sets the UI grid from a 9x9 list of lists and updates the puzzle object.
        """
        self.puzzle.set_grid(grid)
        for i in range(9):
            for j in range(9):
                val = str(grid[i][j]) if grid[i][j] != 0 else ""
                self.cells[i][j].setText(val)

    def set_puzzle_from_string(self, puzzle_str):
        """
        Accepts a string of 81 chars and fills the grid accordingly.
        """
        self.puzzle.set_from_string(puzzle_str)
        self.set_puzzle_from_grid(self.puzzle.get_grid())

    def solve_puzzle(self):
        """
        Calls the solver and animates the solution if successful.
        """
        self.setWindowTitle("PySudoku Solver - Solving...")
        puzzle_str = self.get_puzzle_string()
        self.puzzle.set_from_string(puzzle_str)
        grid = solver.solve_puzzle_obj(self.puzzle)
        if grid and len(grid) == 9 and all(len(row) == 9 for row in grid):
            self.animate_solution(grid)
        else:
            self.setWindowTitle("PySudoku Solver - Failed!")

    def animate_solution(self, grid):
        """
        Animate filling the grid with the solution within 1 second.
        """
        self._anim_i = 0
        self._anim_j = 0
        self._anim_grid = grid
        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._animate_step)
        self._anim_timer.start(12)  # ~12ms per cell for 81 cells in 1s

    def _animate_step(self):
        """
        Animation step: fill one cell per timer tick.
        When finished, check if the puzzle is solved and show the time.
        """
        i, j = self._anim_i, self._anim_j
        val = str(self._anim_grid[i][j]) if self._anim_grid[i][j] != 0 else ""
        self.cells[i][j].setText(val)
        if j < 8:
            self._anim_j += 1
        else:
            self._anim_j = 0
            self._anim_i += 1
        if self._anim_i > 8:
            self._anim_timer.stop()
            if self.timer_running:
                self.timer.stop()
                self.timer_running = False
            if self.is_puzzle_solved():
                mins = self.elapsed_seconds // 60
                secs = self.elapsed_seconds % 60
                self.timer_label.setText(f"Puzzle Finished in: {mins:02d}:{secs:02d}")
                self.setWindowTitle("PySudoku Solver - Success!")
            else:
                self.setWindowTitle("PySudoku Solver - Filled (Not Solved)")
            self.start_btn.setEnabled(False)

    def is_puzzle_solved(self):
        """
        Checks if the current grid is a valid, completely filled Sudoku solution.
        """
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[i][j].text().strip()
                if val in "123456789":
                    row.append(int(val))
                else:
                    return False
            grid.append(row)
        for i in range(9):
            if len(set(grid[i])) != 9:
                return False
            if len(set(grid[j][i] for j in range(9))) != 9:
                return False
        for bi in range(0, 9, 3):
            for bj in range(0, 9, 3):
                block = [grid[bi + x][bj + y] for x in range(3) for y in range(3)]
                if len(set(block)) != 9:
                    return False
        return True

def main():
    """
    Main entry point for the PyQt5 GUI.
    Optionally accepts a puzzle string as a command-line argument.
    """
    app = QApplication(sys.argv)
    puzzle_str = sys.argv[1] if len(sys.argv) > 1 and len(sys.argv[1]) == 81 else None
    window = SudokuUI(puzzle_str)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
