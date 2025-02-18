# Black marbles (14)
black_marbles = [
    (-4,-4,'B'), (-3,-4,'B'), (-2,-4,'B'), (-1,-4,'B'), (0,-4,'B'),
    (-4,-3,'B'), (-3,-3,'B'), (-2,-3,'B'), (-1,-3,'B'), (0,-3,'B'), (1,-3,'B'),
    (-2,-2,'B'), (-2,-1,'B'), (-2,0,'B')
]

# White marbles (14)
white_marbles = [
    (0,4,'W'), (1,4,'W'), (2,4,'W'), (3,4,'W'), (4,4,'W'),
    (-1,3,'W'), (0,3,'W'), (1,3,'W'), (2,3,'W'), (3,3,'W'), (4,3,'W'),
    (0,2,'W'), (1,2,'W'), (2,2,'W')
]

# Initialize the board with all positions as 'N' (neutral/empty)
board = {(x, y): 'N' for x in range(-4, 5) for y in range(-4, 5) if -4 <= x - y <= 4}

# Place black marbles
for (x, y, _) in black_marbles:
    board[(x, y)] = 'B'

# Place white marbles
for (x, y, _) in white_marbles:
    board[(x, y)] = 'W'

# Initial scores [Black,White]
scores = [0, 0]

# Current turn
current_turn = 'Black'

print(board)