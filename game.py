import copy

class Game:
    def __init__(self, initial_state) -> None:
        self.state = initial_state
        self.history = [(initial_state, "Initial state")]

    #test
    def is_within_bounds(self, state, x, y):
        return 0 <= x < state.rows and 0 <= y < state.cols

    def can_move(self, state, x, y):
        return self.is_within_bounds(state, x, y) and state.board[x][y].current_type in ['road', 'solve']

    def move(self, state, new_x, new_y, old_x, old_y, magnet_type):
        updated_state = copy.deepcopy(state)
        updated_state.board[old_x][old_y].current_type = 'road'
        updated_state.board[new_x][new_y].current_type = 'repel' if magnet_type == 'repel' else magnet_type
        if updated_state.board[new_x][new_y].initial_type == 'solve':
            updated_state.board[new_x][new_y].current_type = 'repel'
        
        self.history.append((updated_state, f"Move {magnet_type} magnet to ({new_x}, {new_y})"))
        return updated_state

    def apply_gravity(self, state, x, y):
        updated_state = copy.deepcopy(state)
        for i in range(x - 1, -1, -1):  
            if updated_state.board[i][y].current_type == "iron":
                updated_state.board[i][y].current_type = 'road'
                updated_state.board[i + 1][y].current_type = 'iron'
        for i in range(x + 1, updated_state.rows):  
            if updated_state.board[i][y].current_type == "iron":
                updated_state.board[i][y].current_type = 'road'
                updated_state.board[i - 1][y].current_type = 'iron'

        for j in range(y - 1, -1, -1): 
            if updated_state.board[x][j].current_type == "iron":
                updated_state.board[x][j].current_type = 'road'
                updated_state.board[x][j + 1].current_type = 'iron'
        for j in range(y + 1, updated_state.cols):  
            if updated_state.board[x][j].current_type == "iron":
                updated_state.board[x][j].current_type = 'road'
                updated_state.board[x][j - 1].current_type = 'iron'

        self.history.append((updated_state, f"Apply gravity at ({x}, {y})"))
        return updated_state


    def repel_magnet(self, state, x, y):
        updated_state = copy.deepcopy(state)

        def push_iron(direction):
            dx, dy = direction
            if self.is_within_bounds(updated_state, x + dx, y + dy) and \
               self.is_within_bounds(updated_state, x + 2 * dx, y + 2 * dy) and \
               updated_state.board[x + dx][y + dy].current_type == "iron" and \
               updated_state.board[x + 2 * dx][y + 2 * dy].current_type == "iron":
                
                if self.is_within_bounds(updated_state, x + 3 * dx, y + 3 * dy) and \
                   updated_state.board[x + 3 * dx][y + 3 * dy].current_type in ["road", "solve"]:
                    updated_state.board[x + 3 * dx][y + 3 * dy].current_type = "iron"
                    updated_state.board[x + 2 * dx][y + 2 * dy].current_type = "iron"
                    updated_state.board[x + dx][y + dy].current_type = "road"
                elif updated_state.board[x + 2 * dx][y + 2 * dy].current_type in ["road", "solve"]:
                    updated_state.board[x + 2 * dx][y + 2 * dy].current_type = "iron"
                    updated_state.board[x + dx][y + dy].current_type = "road"
            else:
                for step in range(1, max(updated_state.rows, updated_state.cols)):
                    nx, ny = x + dx * step, y + dy * step
                    if not self.is_within_bounds(updated_state, nx, ny) or \
                       updated_state.board[nx][ny].current_type not in ["road", "solve"]:
                        break
                    if updated_state.board[nx - dx][ny - dy].current_type == "iron":
                        updated_state.board[nx][ny].current_type = "iron"
                        updated_state.board[nx - dx][ny - dy].current_type = "road"
                        break

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            push_iron(direction)

        self.history.append((updated_state, f"Repel at ({x}, {y})"))
        return updated_state

    def move_attract(self, x, y):
        attract_x, attract_y = self.state.getAttractCoord()
        if attract_x is not None and attract_y is not None and self.can_move(self.state, x, y):
            self.state = self.move(self.state, x, y, attract_x, attract_y, "attract")
            self.state = self.apply_gravity(self.state, x, y)
        else:
            print('Invalid move for attract magnet!')

    def move_repel(self, x, y):
        repel_x, repel_y = self.state.getRepelCoord()
        if repel_x is not None and repel_y is not None and self.can_move(self.state, x, y):
            self.state = self.move(self.state, x, y, repel_x, repel_y, "repel")
            self.state = self.repel_magnet(self.state, x, y)
        else:
            print('Invalid move for repel magnet!')

    def print_history(self):
        print("\nHistory of moves:")
        for index, (state, description) in enumerate(self.history):
            print(f"\nMove {index + 1}: {description}")
            print(state)

    def check_win(self):
        for row in self.state.board:
            for cell in row:
                if cell.current_type == "road" and cell.is_Solve:
                    return False
        return True

    def play(self):
        while True:
            print(str(self.state))
            if self.check_win():
                print("Congratulations! You've won the game!")
                self.print_history()
                break

            move_type = input("Enter 'attract' to move the red magnet or 'repel' to move the purple magnet: ")
            new_x = int(input("Enter the new x-coordinate for the magnet: "))
            new_y = int(input("Enter the new y-coordinate for the magnet: "))

            if move_type == 'attract':
                self.move_attract(new_x, new_y)
            elif move_type == 'repel':
                self.move_repel(new_x, new_y)
            else:
                print("Invalid input. Please enter 'attract' or 'repel'.")
