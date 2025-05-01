# sudoku-solver.py
import sys

def is_valid(grid, row, col, num):
    """Check if a number can be placed at grid[row][col]"""
    # Check row
    for x in range(9):
        if grid[row][x] == num:
            return False
    
    # Check column
    for x in range(9):
        if grid[x][col] == num:
            return False
    
    # Check 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    
    return True

def find_placements_for_digit(grid, digit):
    """Find all possible placements for a specific digit"""
    placements = []
    for row in range(9):
        for col in range(9):
            # Only consider empty cells
            if grid[row][col] == 0:
                # Check if digit can be placed here
                if is_valid(grid, row, col, digit):
                    placements.append((row, col))
    return placements

def find_unique_placements_for_digit(grid, digit):
    """Find cells where a digit can ONLY be placed in one position in a row, column, or box"""
    unique_placements = []
    
    # Check rows
    for row in range(9):
        row_placements = []
        for col in range(9):
            if grid[row][col] == 0 and is_valid(grid, row, col, digit):
                row_placements.append((row, col))
        if len(row_placements) == 1:
            unique_placements.append(row_placements[0])
    
    # Check columns
    for col in range(9):
        col_placements = []
        for row in range(9):
            if grid[row][col] == 0 and is_valid(grid, row, col, digit):
                col_placements.append((row, col))
        if len(col_placements) == 1:
            unique_placements.append(col_placements[0])
    
    # Check 3x3 boxes
    for box_row in range(3):
        for box_col in range(3):
            box_placements = []
            start_row, start_col = box_row * 3, box_col * 3
            for i in range(3):
                for j in range(3):
                    row, col = start_row + i, start_col + j
                    if grid[row][col] == 0 and is_valid(grid, row, col, digit):
                        box_placements.append((row, col))
            if len(box_placements) == 1:
                unique_placements.append(box_placements[0])
    
    return unique_placements

def find_missing_digits(grid):
    """Find cells that have only one possible value"""
    placements = []
    
    # Check rows
    for row in range(9):
        # Find missing digits in this row
        digits_in_row = set(grid[row])
        missing_digits = set(range(1, 10)) - digits_in_row
        if 0 in digits_in_row and len(missing_digits) == 1:
            # Find the empty cell
            missing_digit = list(missing_digits)[0]
            for col in range(9):
                if grid[row][col] == 0:
                    placements.append((row, col, missing_digit))
    
    # Check columns
    for col in range(9):
        digits_in_col = set()
        for row in range(9):
            digits_in_col.add(grid[row][col])
        missing_digits = set(range(1, 10)) - digits_in_col
        if 0 in digits_in_col and len(missing_digits) == 1:
            missing_digit = list(missing_digits)[0]
            for row in range(9):
                if grid[row][col] == 0:
                    placements.append((row, col, missing_digit))
    
    # Check 3x3 boxes
    for box_row in range(3):
        for box_col in range(3):
            digits_in_box = set()
            for i in range(3):
                for j in range(3):
                    row, col = box_row * 3 + i, box_col * 3 + j
                    digits_in_box.add(grid[row][col])
            missing_digits = set(range(1, 10)) - digits_in_box
            if 0 in digits_in_box and len(missing_digits) == 1:
                missing_digit = list(missing_digits)[0]
                for i in range(3):
                    for j in range(3):
                        row, col = box_row * 3 + i, box_col * 3 + j
                        if grid[row][col] == 0:
                            placements.append((row, col, missing_digit))
    
    return placements

def solve_with_simple_methods(grid):
    """Solve the puzzle using simple methods"""
    changed = True
    while changed:
        changed = False
        
        # Method 1: Find unique placements for each digit
        for digit in range(1, 10):
            unique_placements = find_unique_placements_for_digit(grid, digit)
            for row, col in unique_placements:
                grid[row][col] = digit
                changed = True
                print(f"Placed {digit} at ({row}, {col}) - unique placement")
        
        # Method 2: Find cells with only one possible value
        missing_placements = find_missing_digits(grid)
        for row, col, digit in missing_placements:
            grid[row][col] = digit
            changed = True
            print(f"Placed {digit} at ({row}, {col}) - missing digit")
    
    return grid

def read_puzzle(file_path):
    grid = []
    with open(file_path, 'r') as file:
        for line in file:
            if '|' not in line or '+' in line:
                continue

            row_data = []
            for char in line:
                if char.isdigit():
                    row_data.append(int(char))
                elif char == '.':
                    row_data.append(0)

            if len(row_data) == 9:
                grid.append(row_data)
    
    return grid

def print_puzzle(grid):
    block_separator = "+-------+-------+-------+"
    print(block_separator)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print(block_separator)
    
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end = "")
            if j == 0:
                print("| ", end="")
            if grid[i][j] == 0:
                print(". ", end="")
            else:
                print(f"{grid[i][j]} ", end="")
            if j == 8:
                print("|")
    
    print(block_separator)

def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku-solver.py <puzzle file>")
        return 1
    
    puzzle_file = sys.argv[1]
    grid = read_puzzle(puzzle_file)

    print("Unsolved Puzzle")
    print_puzzle(grid)

    solved_grid = solve_with_simple_methods(grid)

    print("\nSolved as far as possible with simple methods:")
    print_puzzle(solved_grid)

    if any(0 in row for row in solved_grid):
        print("Puzzle could not be solved.")
    else:
        print("Puzzle solved")
        
if __name__ == '__main__':
    sys.exit(main())