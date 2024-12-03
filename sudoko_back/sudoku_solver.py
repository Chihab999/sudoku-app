class SudokuSolver:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]
        self.original_grid = [row[:] for row in grid]

    def is_valid_move(self, row, col, num):
        # Check row
        for x in range(9):
            if self.grid[row][x] == num:
                return False

        # Check column
        for x in range(9):
            if self.grid[x][col] == num:
                return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False

        return True

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None

    def solve_backtracking(self):
        location = self.find_empty_location()
        if not location:
            return True

        row, col = location
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.grid[row][col] = num

                if self.solve_backtracking():
                    return True

                self.grid[row][col] = 0

        return False

    def solve_bfs(self):
        from queue import Queue

        def serialize_grid(grid):
            return tuple(tuple(row) for row in grid)

        visited = set()
        q = Queue()
        q.put(self.grid)

        while not q.empty():
            current_grid = q.get()

            # Convert grid to tuple for hashability
            grid_state = serialize_grid(current_grid)

            if grid_state in visited:
                continue

            visited.add(grid_state)

            # Check if solution is found
            if self.is_solved(current_grid):
                self.grid = [list(row) for row in current_grid]
                return True

            # Find empty cell
            empty_cell = self.find_empty_location_in_grid(current_grid)
            if not empty_cell:
                continue

            row, col = empty_cell

            # Try all possible numbers
            for num in range(1, 10):
                if self.is_valid_move_in_grid(current_grid, row, col, num):
                    new_grid = [row[:] for row in current_grid]
                    new_grid[row][col] = num
                    q.put(new_grid)

        return False

    def solve_dfs(self):
        def dfs_solve(grid):
            location = self.find_empty_location_in_grid(grid)
            if not location:
                return grid

            row, col = location
            for num in range(1, 10):
                if self.is_valid_move_in_grid(grid, row, col, num):
                    grid[row][col] = num
                    result = dfs_solve(grid)
                    if result:
                        return result
                    grid[row][col] = 0

            return None

        result = dfs_solve(self.grid)
        if result:
            self.grid = result
            return True
        return False

    def is_solved(self, grid):
        for row in grid:
            if 0 in row:
                return False
        return True

    def find_empty_location_in_grid(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return i, j
        return None

    def is_valid_move_in_grid(self, grid, row, col, num):
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

    def solve(self, algorithm='backtracking'):
        if algorithm == 'backtracking':
            return self.solve_backtracking()
        elif algorithm == 'bfs':
            return self.solve_bfs()
        elif algorithm == 'dfs':
            return self.solve_dfs()
        else:
            raise ValueError("Invalid algorithm. Choose 'backtracking', 'bfs', or 'dfs'.")

    def get_solution(self):
        return self.grid