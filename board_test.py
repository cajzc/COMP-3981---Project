# # Black marbles (14)
# black_marbles = [
#     (-4,-4,'b'), (-3,-4,'b'), (-2,-4,'b'), (-1,-4,'b'), (0,-4,'b'),
#     (-4,-3,'b'), (-3,-3,'b'), (-2,-3,'b'), (-1,-3,'b'), (0,-3,'b'), (1,-3,'b'),
#     (-2,-2,'b'), (-2,-1,'b'), (-2,0,'b')
# ]
#
# # White marbles (14)
# white_marbles = [
#     (0,4,'w'), (1,4,'w'), (2,4,'w'), (3,4,'w'), (4,4,'w'),
#     (-1,3,'w'), (0,3,'w'), (1,3,'w'), (2,3,'w'), (3,3,'w'), (4,3,'w'),
#     (0,2,'w'), (1,2,'w'), (2,2,'w')
# ]


#
# # Place black marbles
# for (x, y, _) in black_marbles:
#     board[(x, y)] = 'b'
#
# # Place white marbles
# for (x, y, _) in white_marbles:
#     board[(x, y)] = 'w'



def main():
    # Initial scores [black,white]
    scores = [0, 0]

    # # Initialize the board with all positions as 'N' (neutral/empty)
    # board = {(x, y): 'N' for x in range(-4, 5) for y in range(-4, 5) if -4 <= x - y <= 4}

    with open('Test1.input','r') as f:
        player = f.readline().strip()
        marbles = f.readline().strip().split(',')
    print(marbles)

    board = {(int(marble[1]),  ord(marble[0]) - ord('E')): marble[2] for marble in marbles}

    # Current turn
    current_turn = player

    print(board)


if __name__ == '__main__':
    main()

