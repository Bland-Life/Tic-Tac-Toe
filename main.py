import math

print("Welcome to Tic Tac Toe, to play begin by typing in the number you'd like to replace\n")

grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

def swap_player(player):
    if player == 'O':
        return 'X'
    elif player == 'X':
        return 'O'


def check_horizonal_match(grid):
    for axis in grid:
        if len(set(axis)) == 1:
            return True
    return False


def check_vertical_match(grid):
    vertical_match = [
        index for index, (e1, e2, e3) in enumerate(zip(grid[0], grid[1], grid[2]))
        if e1 == e2 and e2 == e3
    ]
    if vertical_match:
        return True
    return False


def check_diagonal_match(grid):
    if grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2]:
        return True
    elif grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0]:
        return True
    else:
        return False


def grid_full(grid):
    not_full = None
    for axis in grid:
        not_full = True if [i for i in axis if type(i) == int] else False
        if not_full:
            return False
    return True

current_player = 'O'
while True:
    text_field = f'\n{grid[0][0]} | {grid[0][1]} | {grid[0][2]}\n'\
  '---------\n' \
    f'{grid[1][0]} | {grid[1][1]} | {grid[1][2]}\n' \
  '---------\n' \
    f'{grid[2][0]} | {grid[2][1]} | {grid[2][2]}\n'

    print(text_field)

    if check_diagonal_match(grid) or check_horizonal_match(
        grid) or check_vertical_match(grid):
        print(f'{current_player} Wins!')
        break
    elif grid_full(grid):
        print('No one wins...')
        break

    current_player = swap_player(current_player)
    place = int(input(f"{current_player}'s move, type here: "))
    grid_index = math.ceil(place / 3) - 1
    axis_index = (place % 3) - 1
    grid[grid_index][axis_index] = current_player