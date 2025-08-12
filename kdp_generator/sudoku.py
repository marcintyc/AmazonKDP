import random
from typing import List, Tuple

from .pdf_utils import create_canvas, size_to_points, draw_footer_page_number, DEFAULT_MARGIN, draw_page_title

Grid = List[List[int]]


def is_valid(grid: Grid, r: int, c: int, val: int) -> bool:
    for i in range(9):
        if grid[r][i] == val or grid[i][c] == val:
            return False
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if grid[i][j] == val:
                return False
    return True


def find_empty(grid: Grid) -> Tuple[int, int]:
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return -1, -1


def solve(grid: Grid, count_solutions: bool = False, limit: int = 2) -> int:
    r, c = find_empty(grid)
    if r == -1:
        return 1
    nums = list(range(1, 10))
    random.shuffle(nums)
    total = 0
    for v in nums:
        if is_valid(grid, r, c, v):
            grid[r][c] = v
            total += solve(grid, count_solutions, limit)
            if total >= limit:
                grid[r][c] = 0
                return total
            grid[r][c] = 0
    return total


def fill_complete_grid() -> Grid:
    grid = [[0] * 9 for _ in range(9)]

    def backtrack() -> bool:
        r, c = find_empty(grid)
        if r == -1:
            return True
        nums = list(range(1, 10))
        random.shuffle(nums)
        for v in nums:
            if is_valid(grid, r, c, v):
                grid[r][c] = v
                if backtrack():
                    return True
                grid[r][c] = 0
        return False

    backtrack()
    return grid


def make_puzzle(difficulty: str = "easy") -> Grid:
    full = fill_complete_grid()
    puzzle = [row[:] for row in full]

    if difficulty == "easy":
        target_clues = random.randint(36, 40)
    else:
        target_clues = random.randint(30, 34)

    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)

    clues = 81
    for r, c in positions:
        if clues <= target_clues:
            break
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        grid_copy = [row[:] for row in puzzle]
        num_solutions = solve(grid_copy, count_solutions=True, limit=2)
        if num_solutions != 1:
            puzzle[r][c] = backup
        else:
            clues -= 1
    return puzzle


def render_sudoku_pdf(puzzles: List[Grid], filename: str, trim_size: str = "8.5x11"):
    canvas = create_canvas(filename, trim_size)
    page_width, page_height = size_to_points(trim_size)
    margin = DEFAULT_MARGIN

    grid_size = min(page_width, page_height) - 2 * margin
    cell_size = grid_size / 9
    origin_x = (page_width - grid_size) / 2
    origin_y = (page_height - grid_size) / 2

    page_num = 1
    for puzzle in puzzles:
        draw_page_title(canvas, page_width, page_height, "Sudoku")
        for r in range(10):
            lw = 2 if r % 3 == 0 else 1
            canvas.setLineWidth(lw)
            y = origin_y + r * cell_size
            canvas.line(origin_x, y, origin_x + grid_size, y)
        for c in range(10):
            lw = 2 if c % 3 == 0 else 1
            canvas.setLineWidth(lw)
            x = origin_x + c * cell_size
            canvas.line(x, origin_y, x, origin_y + grid_size)
        canvas.setFont("Helvetica", 14)
        for r in range(9):
            for c in range(9):
                v = puzzle[r][c]
                if v != 0:
                    text = str(v)
                    x = origin_x + c * cell_size + cell_size / 2
                    y = origin_y + (8 - r) * cell_size + cell_size * 0.3
                    canvas.drawCentredString(x, y, text)
        draw_footer_page_number(canvas, page_width, margin, page_num)
        canvas.showPage()
        page_num += 1
    canvas.save()