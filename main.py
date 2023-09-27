import math, random
import gridlogic as gl

print("Welcome to Tic Tac Toe, to play begin by typing in the number you'd like to replace\n")
print("Automatic Game Mode Enabled")

grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def swap_player(player):
    if player == 'O':
        return 'X'
    elif player == 'X':
        return 'O'


current_player = 'O'
open_spots = [1, 2, 3, 4, 5, 6, 7, 8, 9]
while True:
    text_field = f'\n{grid[0][0]} | {grid[0][1]} | {grid[0][2]}\n'\
  '---------\n' \
    f'{grid[1][0]} | {grid[1][1]} | {grid[1][2]}\n' \
  '---------\n' \
    f'{grid[2][0]} | {grid[2][1]} | {grid[2][2]}\n'

    print(text_field)

    if gl.check_diagonal_match(grid) or gl.check_horizonal_match(
        grid) or gl.check_vertical_match(grid):
        print(f'{current_player} Wins!')
        break
    elif gl.grid_full(grid):
        print('Draw!')
        break

    current_player = swap_player(current_player)
    while True:
        if current_player == 'O':
            priority_spots = gl.almost_match(grid, computer=current_player, player=swap_player(current_player))
            if priority_spots:
                place = random.choice(priority_spots)
            else:
                place = random.choice(open_spots)
        else:
            place = int(input(f"{current_player}'s move, type here: "))
        if place not in open_spots:
            print(place)
            print("Not Open, Try Again.")
        else:
            break
    open_spots.pop(open_spots.index(place))
    grid_index = math.ceil(place / 3) - 1
    axis_index = (place % 3) - 1
    grid[grid_index][axis_index] = current_player