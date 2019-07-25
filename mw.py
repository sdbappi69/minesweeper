import random
import re
import time

def showGrid(grid):
    grid_row_size = len(grid)
    grid_col_size = len(grid[0])

    horizontal = '   ' + (6 * grid_col_size * '-') + '-'

    # Print top column letters
    col_label = '     '
    for i in range(1, grid_col_size+1):
        col_label = col_label + "{0:0=2d}".format(i) + '    '
    print(col_label + '\n' + horizontal)

    # Print left row numbers
    for idx, i in enumerate(grid):
        row_label = "{0:0=2d}".format(idx + 1)
        row = '{0:2} |'.format(row_label)

        for j in i:
            row = row + '  ' + j + '  |'

        print(row + '\n' + horizontal)

    print('')

def parseInput(column_prompt, row_prompt, flag_prompt, row_count, column_count, help_msg):
    cell = ()
    flag = False
    message = "Invalid cell. " + help_msg

    row_no = int(row_prompt) - 1
    col_no = int(column_prompt) - 1

    if flag_prompt == 'y':
        flag = True

    if -1 < row_no < row_count:
        if -1 < col_no < column_count:
            cell = (row_no, col_no)
            message = ''

    return {'cell': cell, 'flag': flag, 'message': message}

def setupGrid(row_count, column_count, start, mine_count):
    empty_grid = [['0' for i in range(column_count)] for i in range(row_count)]

    mines = getMines(empty_grid, start, mine_count)

    for i, j in mines:
        empty_grid[i][j] = 'X'

    grid = getNumbers(empty_grid)

    return (grid, mines)


def getRandomCell(grid):
    grid_row_size = len(grid)
    grid_col_size = len(grid[0])

    a = random.randint(0, grid_row_size - 1)
    b = random.randint(0, grid_col_size - 1)

    return (a, b)


def getNeighbors(grid, row_no, col_no):
    grid_row_size = len(grid)
    grid_col_size = len(grid[0])
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (row_no + i) < grid_row_size and -1 < (col_no + j) < grid_col_size:
                neighbors.append((row_no + i, col_no + j))

    return neighbors


def getMines(grid, start, mine_count):
    mines = []
    neighbors = getNeighbors(grid, *start)

    for i in range(mine_count):
        cell = getRandomCell(grid)
        while cell == start or cell in mines or cell in neighbors:
            cell = getRandomCell(grid)
        mines.append(cell)

    return mines


def getNumbers(grid):
    for row_no, row in enumerate(grid):
        for col_no, cell in enumerate(row):
            if cell != 'X':
                # Gets the values of the neighbors
                values = [grid[r][c] for r, c in getNeighbors(grid,
                                                              row_no, col_no)]

                # Counts how many are mines
                grid[row_no][col_no] = str(values.count('X'))

    return grid


def showCells(grid, curr_grid, row_no, col_no):
    # Exit function if the cell was already shown
    if curr_grid[row_no][col_no] != ' ':
        return

    # Show current cell
    curr_grid[row_no][col_no] = grid[row_no][col_no]

    # Get the neighbors if the cell is empty
    if grid[row_no][col_no] == '0':
        for r, c in getNeighbors(grid, row_no, col_no):
            # Repeat function for each neighbor that doesn't have a flag
            if curr_grid[r][c] != 'F':
                showCells(grid, curr_grid, r, c)


def playagain():
    choice = input('Play again? (y/n): ')

    return choice.lower() == 'y'


def startGame(row_count, column_count, mine_count):
    # Introduction
    print("Welcome to MineSweeper. Let's Play!")

    curr_grid = [[' ' for i in range(column_count)] for i in range(row_count)]

    grid = []
    flags = []
    start_time = 0

    # Initiate the board
    showGrid(curr_grid)

    # Help message for the user
    help_msg = ("Enter the Row(Left) number first then the Column(Top). "
                   "To put or remove a flag, Enter 'y' to the 'Flag' promt")
    print(help_msg)

    while True:
        mines_left = mine_count - len(flags)
        row_prompt = input('Enter the Row(Left) number: ')
        column_prompt = input('Enter the Column(Top) number: ')
        flag_prompt = input('Add/Remove the Flag (y/*): ')
        result = parseInput(column_prompt, row_prompt, flag_prompt, row_count, column_count, help_msg + '\n')

        # print(result)

        message = result['message']
        cell = result['cell']

        print("Status: " + str(mines_left) + "mines left")

        if cell:
            print('\n\n')
            row_no, col_no = cell
            curr_cell = curr_grid[row_no][col_no]
            flag = result['flag']

            if not grid:
                grid, mines = setupGrid(row_count, column_count, cell, mine_count)
            if not start_time:
                start_time = time.time()

            if flag:
                # Add a flag if the cell is empty
                if curr_cell == ' ':
                    curr_grid[row_no][col_no] = 'F'
                    flags.append(cell)
                # Remove the flag if there is one
                elif curr_cell == 'F':
                    curr_grid[row_no][col_no] = ' '
                    flags.remove(cell)
                else:
                    message = 'Cannot put a flag there'

            # If there is a flag there, show a message
            elif cell in flags:
                message = 'There is a flag there'

            elif grid[row_no][col_no] == 'X':
                print('Game Over\n')
                showGrid(grid)
                if playagain():
                    startGame(row_count, column_count, mine_count)
                return

            elif curr_cell == ' ':
                showCells(grid, curr_grid, row_no, col_no)

            else:
                message = "That cell is already shown"

            if set(flags) == set(mines):
                minutes, seconds = divmod(int(time.time() - start_time), 60)
                print(
                    'You Win. '
                    'It took you {} minutes and {} seconds.\n'.format(minutes,
                                                                      seconds))
                showGrid(grid)
                if playagain():
                    startGame(row_count, column_count, mine_count)
                return

        showGrid(curr_grid)
        print(message)



# Initialize the game
row_count = 20
column_count = 30
mine_count = 25
startGame(row_count, column_count, mine_count)