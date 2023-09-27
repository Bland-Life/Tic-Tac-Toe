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


def almost_match(grid, computer,  player):

    win_conditions = []
    lose_conditions = []

    # Checks for near-horizontal matches
    for axis in grid:
        if axis.count(computer) > 1:
            if axis.count(player) != 1:   
                [win_conditions.append(spot) for spot in axis if spot != computer and spot != player]
        elif axis.count(player) > 1:
            if axis.count(computer) != 1:   
                [lose_conditions.append(spot) for spot in axis if spot != computer and spot != player]
        
        
    vertical_grid = [
        [e1, e2, e3] for (e1, e2, e3) in zip(grid[0], grid[1], grid[2])
    ]

    # Checks for near-vertical matches
    for axis in vertical_grid:
        if axis.count(computer) > 1:
            if axis.count(player) != 1:   
                [win_conditions.append(spot) for spot in axis if spot != computer and spot != player]
        elif axis.count(player) > 1:
            if axis.count(computer) != 1:   
                [lose_conditions.append(spot) for spot in axis if spot != computer and spot != player]
        
    #Checks for near-diagonal matches
    diagonals = []
    diagonals.append([grid[x][y] for (x, y) in zip(range(0, 3), range(0, 3))])
    diagonals.append([grid[x][y] for (x, y) in zip(range(0, 3), range(2, -1, -1))])
    for axis in diagonals:
        if axis.count(computer) > 1:
            if axis.count(player) != 1:   
                [win_conditions.append(spot) for spot in axis if spot != computer and spot != player]
        elif axis.count(player) > 1:
            if axis.count(computer) != 1:   
                [lose_conditions.append(spot) for spot in axis if spot != computer and spot != player]
        
    if win_conditions:
        return win_conditions
    else:
        return lose_conditions