from cell import Cells
from game import Game
from state import State

def create_level(init_board):
    rows = len(init_board)
    cols = len(init_board[0])
    board = [[None for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            cell_data = init_board[i][j]
            board[i][j] = Cells(i, j, cell_data['type'], cell_data['is_Solve'])
    return State(rows, cols, board)

levels = [
    [
        [{'type': 'iron', 'is_Solve': False}, {'type': 'road', 'is_Solve': False}, {'type': 'block', 'is_Solve': False}, {'type': 'block', 'is_Solve': False}, {'type': 'block', 'is_Solve': False}],
        [{'type': 'iron', 'is_Solve': True}, {'type': 'road', 'is_Solve': False}, {'type': 'block', 'is_Solve': False}, {'type': 'block', 'is_Solve': False}, {'type': 'block', 'is_Solve': False}],
        [{'type': 'road', 'is_Solve': True}, {'type': 'road', 'is_Solve': False}, {'type': 'road', 'is_Solve': False}, {'type': 'road', 'is_Solve': False}, {'type': 'block', 'is_Solve': False}],
        [{'type': 'road', 'is_Solve': False}, {'type': 'attract', 'is_Solve': False}, {'type': 'road', 'is_Solve': False}, {'type': 'road', 'is_Solve': False}, {'type': 'block', 'is_Solve': False}],
        [{'type': 'road', 'is_Solve': True}, {'type': 'road', 'is_Solve': False}, {'type': 'road', 'is_Solve': True}, {'type': 'iron', 'is_Solve': False}, {'type': 'block', 'is_Solve': False}]
    ]
]


print("choose level")
for index, level in enumerate(levels):
    print(f"{index + 1}: level {index + 1}")

level_choice = int(input("enter the number of level: ")) - 1
if level_choice < 0 or level_choice >= len(levels):
    print("number invalid automatically will present the level 1")
    level_choice = 0

init_state = create_level(levels[level_choice])
print("Initial state:")
print(init_state)

game = Game(init_state)
game.play()
