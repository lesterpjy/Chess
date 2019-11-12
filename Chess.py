import sys
import os
from itertools import cycle
# References:
# https://docs.python.org/3/library/sys.html
# https://docs.python.org/3/library/itertools.html
# https://en.wikipedia.org/wiki/Chess

class interactive:
    '''Interactive class

    Encapsulates most user interactions: beginning game, move inputs, etc.
    Methods: move_parse, disambiguate
    '''

    def __init__(self):
        '''init for interactive class

        Initialize game with on-screen instructions,
        take user inputs to begin/end game.
        '''

        print("----------------------------------")
        print("Welcome to the Chess app! ♕")
        print("----------------------------------")
        print("The game is able to detect check,\n"
              "but may occasionally fail to detect checkmate,"
              "if this happens, please enter 'end' to exit the app at 'Please enter a move' prompt.")
        while True:
            print("Enter '1' to play a game of chess, and enter 'end' to exit.")
            user = input("What would you like to do? ")
            print("----------------------------------")
            if user == '1':
                print("White always plays first move!")
                player1 = input("Enter white set player name: ")
                color1 = 'white'
                player2 = input("Enter black set player name: ")
                color2 = 'black'
                print("----------------------------------")
                print("Initializing a game of chess with " +
                      player1 + " as " + color1 + ", and " +
                      player2 + " as " + color2 + ". ")
                print("----------------------------------")
                # Initialize a game of chess and print board.
                game = chess(player1, color1, player2, color2)
                print(game)
                print("----------------------------------")
                print("This game of chess follows the standard chess rules, and requires 2 people to play.")
                print("Enter each move with the standard algebraic chess notation.")
                print("For example, the pawn at e2 is moved to e4 with the command 'e4'.")
                print("The knight at g1 can be moved to f3 with the command 'Nf3'")
                print("Capture is represented with 'x', for example, 'Bxc6' is the command for bishop to capture a piece at c6.")
                print("To castle, simply enter 'o-o'.")
                print("----------------------------------")
                print("The algebraic letter for each piece are:\n", chess.p_fig_map)
                print("For more information on the notation, please visit:\nhttps://en.wikipedia.org/wiki/Algebraic_notation_(chess)")
                print("----------------------------------")
                yn = input("Now let us start the game? (enter y/n) ").lower()
                print("----------------------------------")
                if yn == 'y':
                    game.main()
                    print("Thank you for playing!")
                    sys.exit(0)
                elif yn != 'y':
                    pass
            elif user == 'end':
                print("Thank you for playing!")
                sys.exit(0)
            else:
                print("""Error: Enter 1 to play a game of chess, and enter end() to exit.""")

    def move_parse(mv_cmd, pos_dict):
        '''Parse user command to move a chess piece

        keyword arg:
        mv_cmd -- user command as a string
        pos_dict -- position dictionary mapping alpha to num.
        '''

        mv_cmd_list = list(mv_cmd)
        # Check if command is a 'pawn capture' move.
        if mv_cmd_list[1] == 'x' and mv_cmd_list[0] not in 'rnbqk':
            mv_cmd_list.insert(0, 'p')
            new_pos = (pos_dict[mv_cmd_list[-2]], int(mv_cmd_list[-1]))
            out_list = mv_cmd_list[:-2]
            out_list.append(new_pos)
            # Returning command as list with shorthand of piece,
            # and a tuple of new position
            return out_list
        # Check if command is a pawn move.
        elif mv_cmd_list[0] not in 'rnbqk':
            mv_cmd_list.insert(0, 'p')
            new_pos = (pos_dict[mv_cmd_list[-2]], int(mv_cmd_list[-1]))
            out_list = mv_cmd_list[:-2]
            out_list.append(new_pos)
            # Returning command as list with shorthand of piece,
            # and a tuple of new position
            return out_list
        # All other moves.
        else:
            if len(mv_cmd_list) == 2:
                mv_cmd_list.insert(0, 'p')
            new_pos = (pos_dict[mv_cmd_list[-2]], int(mv_cmd_list[-1]))
            out_list = mv_cmd_list[:-2]
            out_list.append(new_pos)
            # Returning command as list with shorthand of piece,
            # and a tuple of new position
            return out_list

    def disambiguate(list_to_disambiguate, case):
        '''Disambiguate user intent
        Either multiple piece can achieve the same move,
        or King can castle to both rooks.

        keyword arg:
        list_to_disambiguate -- list of possibilities.
        case -- argument passing which kind of disambiguation.
        '''
        pos_dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
        while True:
            try:
                if case == 1:
                    print("More than one piece can achieve the move, please disambiguate.")
                    # iterate through list to ask which the user wants
                    for i in range(len(list_to_disambiguate)):
                        name = list_to_disambiguate[i].piece_name
                        pos = pos_dict[list_to_disambiguate[i].pos[0]] + str(list_to_disambiguate[i].pos[1])
                        print(str(i) + ". {} at {} can be moved.".format(name, pos))
                    choice = int(input("Please choose from the above 0, 1,.... Enter just '1' to choose 1. "))
                    # check user choice
                    assert choice in range(len(list_to_disambiguate))
                    return list_to_disambiguate[choice]
                elif case == 2:
                    # show list to ask which the user wants
                    pos1 = pos_dict[list_to_disambiguate[0][0]] + str(list_to_disambiguate[0][1])
                    pos2 = pos_dict[list_to_disambiguate[1][0]] + str(list_to_disambiguate[1][1])
                    print("The King can castle either way, please disambiguate.")
                    print("King can Castle to {} or {}.".format(pos1, pos2))
                    choice = int(input("Enter '0' or '1' to choose from {} or {}, respectively.".format(pos1, pos2)))
                    # check user choice
                    assert choice in (0, 1)
                    return list_to_disambiguate[choice]
            except:
                print("Please enter command following on-screen instructions.")
                print("----------------------------------")

class chess:
    '''Chess class

    Contains main game mechanics:
    initializing board, printing board, main game cycle,
    piece moving, and checking check.
    Methods: initialize_board, __str__, main, move_piece, check
    '''
    pos_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    p_fig_map = {'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕',
                 'K': '♔', 'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝',
                 'q': '♛', 'k': '♚', '.': '.'}

    def __init__(self, player_name1, color1, player_name2, color2):
        '''Initialze a game
        with players and set colors
        '''
        self.player1 = player(player_name1, color1)
        self.player2 = player(player_name2, color2)
        self.board = {}
        self.initialize_board()

    def initialize_board(self):
        '''Initialze the board dictionary
        with tuples as keys and piece classes as values
        '''
        init_order = [Rook, Knight, Bishop, Queen,
                      King, Bishop, Knight, Rook]
        cls_p_map = {Rook: 'r', Knight: 'n', Bishop: 'b', Queen: 'q', King: 'k', Pawn: 'p'}
        # Initialze position of pawns
        for i in range(1, 9):
            self.board[(i, 2)] = Pawn(cls_p_map[Pawn], self.player1.color, (i, 2))
            self.board[(i, 7)] = Pawn(cls_p_map[Pawn], self.player2.color, (i, 7))
        # Initialze position of all other pieces
        for i in range(1, 9):
            self.board[(i, 1)] = init_order[i-1](cls_p_map[init_order[i-1]], self.player1.color, (i, 1))
            self.board[(i, 8)] = init_order[i-1](cls_p_map[init_order[i-1]], self.player2.color, (i, 8))

    def __str__(self):
        '''Print board
        Align figurines and file/rank indices
        '''
        board_print = ['   a b c d e f g h']
        # iterate through the ranks from 8 to 1
        for i in range(8, 0, -1):
            str_temp = str(i)+'  '
            # iterate through the files from 1 to 8
            for j in range(1, 9):
                str_temp += self.p_fig_map[self.board.get((j, i), ".").__str__()]
                str_temp += ' '
            str_temp = str_temp + ' ' + str(i)
            board_print.append(str_temp)
        return "\n".join(board_print) + '\n   a b c d e f g h\n'

    def main(self):
        '''Main mechanics
        Cycle user turns, castling move, find pieces
        '''

        # Cycle turns
        for player in cycle([self.player1, self.player2]):
            while True:
                while True:
                    try:
                        # take user command for performing basic checking
                        # if the command is valid, if end is called
                        print(player.color[0].upper() + player.color[1:] + " to move.")
                        mv_cmd = input("Please enter a move in standard algebraic notation: ").lower()
                        if mv_cmd == 'end':
                            print("Thank you for playing!")
                            sys.exit(0)
                        elif mv_cmd[-2] in 'abcdefgh' and mv_cmd[-1] in '12345678':
                            break
                        elif mv_cmd[0] == 'o' and mv_cmd[-1] == 'o':
                            break
                    except SystemExit as e:
                        sys.exit(e)
                    except:
                        print("Error: please input with standard algebraic notation, ex: 'e4' or 'Nf3'.")
                # if the user does not want to castle the king
                if not (mv_cmd[0] == 'o' and mv_cmd[-1] == 'o'):
                    # pasrse command to list and tuple
                    mv_cmd_list = interactive.move_parse(mv_cmd, self.pos_dict)
                    # find all possible pieces that are ther user's
                    possible_piece = [x for x in self.board.values() if x.piece_name == mv_cmd_list[0] and x.color == player.color]
                    # find pieces in the possible pieces that can complete the move
                    piece_to_mv = [x for x in possible_piece if mv_cmd_list[-1] in x.available_moves(self)]
                    # if 'pawn capture'
                    if 'x' in mv_cmd_list and mv_cmd_list[0] == 'p':
                        piece_to_mv = [x for x in piece_to_mv if x.pos[0] == self.pos_dict[mv_cmd_list[1]]]
                    # if there are only one piece, ie, no ambiguity
                    if len(piece_to_mv) == 1:
                        self.move_peice(piece_to_mv[0], mv_cmd_list[-1], mv_cmd_list[0], player.color)
                        break
                    # ask user to disambiguate
                    elif len(piece_to_mv) > 1:
                        exact_piece = interactive.disambiguate(piece_to_mv, 1)
                        self.move_peice(exact_piece, mv_cmd_list[-1], mv_cmd_list[0], player.color)
                        break
                    # No piece can complete the move, ask to input again
                    elif not piece_to_mv:
                        # clear screen
                        os.system('clear')
                        print("Error: Invalid move, please enter another.")
                        print(self)
                        print("----------------------------------")
                # if the user wants to castle the king
                else:
                    # find the user's king
                    the_king = [x for x in self.board.values() if x.piece_name == 'k' and x.color == player.color]
                    # find the user's rooks
                    the_rooks = [x for x in self.board.values() if x.piece_name == 'r' and x.color == player.color]
                    rook_pos = [(1, 1), (1, 8), (8, 1), (8, 8)]
                    # check rooks are in position
                    possible_rooks = [rk for rk in the_rooks if rk.pos in rook_pos]
                    # check king is in position
                    if the_king[0].pos in [(5, 1), (4, 8)] and len(possible_rooks) > 0:
                        castle_1, castle_2 = [], []
                        # check the path is cleared if user is white set.
                        if player.color == 'white':
                            if all([(the_king[0].pos[0]+j, the_king[0].pos[1]) not in self.board.keys() for j in [1, 2]]):
                                castle_1 = [(the_king[0].pos[0]+2, the_king[0].pos[1])]
                            if all([(the_king[0].pos[0]-j, the_king[0].pos[1]) not in self.board.keys() for j in [1, 2, 3]]):
                                castle_2 = [(the_king[0].pos[0]-2, the_king[0].pos[1])]
                        # check the path is cleared if user is white set.
                        else:
                            if all([(the_king[0].pos[0]+j, the_king[0].pos[1]) not in self.board.keys() for j in [1, 2, 3]]):
                                castle_1 = [(the_king[0].pos[0]+2, the_king[0].pos[1])]
                            if all([(the_king[0].pos[0]-j, the_king[0].pos[1]) not in self.board.keys() for j in [1, 2]]):
                                castle_2 = [(the_king[0].pos[0]-2, the_king[0].pos[1])]
                        # if both rooks can be reached, ask user to disambiguate, then castle.
                        if castle_1 and castle_2:
                            castle_to = interactive.disambiguate([castle_1[0], castle_2[0]], 2)
                            if castle_to == castle_1[0]:
                                rook_to_move = [rk for rk in possible_rooks if rk.pos[0] == 8]
                                self.move_peice(the_king[0], castle_to, 'k', player.color, castling=True, rook=rook_to_move[0])
                                break
                            else:
                                rook_to_move = [rk for rk in possible_rooks if rk.pos[0] == 1]
                                self.move_peice(the_king[0], castle_to, 'k', player.color, castling=True, rook=rook_to_move[0])
                                break
                        # Only one rook can be reached, castle
                        elif castle_1 and not castle_2:
                            castle_to = castle_1[0]
                            rook_to_move = [rk for rk in possible_rooks if rk.pos[0] == 8]
                            self.move_peice(the_king[0], castle_to, 'k', player.color, castling=True, rook=rook_to_move[0])
                            break
                        # Only one rook can be reached, castle
                        elif castle_2 and not castle_1:
                            castle_to = castle_2[0]
                            rook_to_move = [rk for rk in possible_rooks if rk.pos[0] == 1]
                            self.move_peice(the_king[0], castle_to, 'k', player.color, castling=True, rook=rook_to_move[0])
                            break
                        else:
                            print("Cannot castle, please re-enter your move.")
                    else:
                        print("Cannot castle, please re-enter your move.")
            # clear screen
            os.system('clear')
            # check if check, and print warning.
            checking_p = self.check(player.color)
            if checking_p:
                # if check, check if checkmate
                if self.checkmate(player.color, checking_p):
                    print(self)
                    print("Checkmate! " + player.player_name + " has won.")
                    break
                else:
                    if player.color == 'black': print("White King in check!")
                    elif player.color == 'white': print("Black King in check!")
            print(self)
            print("----------------------------------")

    def move_peice(self, piece_to_del, pos_to_move, piece_name, p_color, castling=False, rook=None):
        """Move pice
        by deleting key of original position,
        and adding new piece object to board dictionary at new position.

        keywoard arg:
        piece_to_del -- piece object to be moved
        pos_to_move -- tuple for new position
        piece_name -- shorthand name of object to be moved
        p_color -- color of user set
        castling -- if move is castling
        rook -- rook object to be moved
        """

        p_cls_map = {'r': Rook, 'n': Knight, 'b': Bishop, 'q': Queen, 'k': King, 'p': Pawn}
        # if move is castling, move both rook and king
        if castling:
            del self.board[piece_to_del.pos]
            self.board[pos_to_move] = p_cls_map[piece_name](piece_name, p_color, pos_to_move)
            if rook.pos[0] == 8:
                file = -1
            else:
                file = 1
            del self.board[rook.pos]
            pos_to_move = (pos_to_move[0]+file, pos_to_move[1])
            self.board[pos_to_move] = p_cls_map['r']('r', p_color, pos_to_move)
        # otherwise move the piece

        else:
            del self.board[piece_to_del.pos]
            self.board[pos_to_move] = p_cls_map[piece_name](piece_name, p_color, pos_to_move)

    def check(self, p_color):
        """Check if check is established
        by finding position of king,
        and if opponent's pieces can reach that position.

        keyword arg:
        p_color -- user's set color.
        """

        # find opponent king
        king = [x for x in self.board.values() if x.piece_name == 'k' and x.color != p_color]
        # find all my pieces
        my = [x for x in self.board.values() if x.color == p_color]
        # if my piece can reach the king
        for e in my:
            if king[0].pos in e.available_moves(self):
                return (e, king[0])
        return False

    def checkmate(self, p_color, checking_p):
        '''Check is checkmate is established
        Three ways to get out of check:
            1. Capturing checking piece.
            2. Moving the King to not-in-check space.
            3. Blocking the check.

        It is possible that this method does not cover all possibilities,
        and fail to recognize a checkmate.
        '''
        #print("checking checkmate")
        # find all my pieces
        my = [x for x in self.board.values() if x.color == p_color]
        # find all opponent pieces
        op = [x for x in self.board.values() if x.color != p_color and x.piece_name != 'k']
        # can my checking piece be captured?
        if [e for e in op if checking_p[0].pos in e.available_moves(self)]:
            #print("cap")
            return False
        # can the king be moved to where all my piece cannot reach
        all_possible_moves = [move for e in my for move in e.available_moves(self)]
        if [k_new_pos for k_new_pos in checking_p[1].available_moves(self) if k_new_pos not in all_possible_moves]:
            #print("moved")
            return False

        # Can opponent piece block the check
        # My checking piece not a knight and on same file
        if checking_p[0].piece_name != 'n' and checking_p[0].pos[0] == checking_p[1].pos[0]:
            # can opponent piece reach the same file
            for e in op:
                if [move for move in e.available_moves(self) if move[0] == checking_p[1].pos[0]]:
                    #print("file")
                    return False
        # My checking piece not a knight and on same rank
        elif checking_p[0].piece_name != 'n' and checking_p[0].pos[1] == checking_p[1].pos[1]:
            # can opponent piece reach the same rank
            for e in op:
                if [move for move in e.available_moves(self) if move[1] == checking_p[1].pos[1]]:
                    #print("rank")
                    return False
        # My checking piece not a knight and not on same file or rank
        elif checking_p[0].piece_name != 'n':
            # find the base move my checking piece use to reach opponent king
            for move in checking_p[0].available_moves(self):
                if move == checking_p[1].pos:
                    delta_file = (move[0] - checking_p[0].pos[0]) / abs((move[0] - checking_p[0].pos[0]))
                    delta_rank = (move[1] - checking_p[0].pos[1]) / abs((move[1] - checking_p[0].pos[1]))
                    # Store all diagonal between checking piece and opponent king
                    diagonal = [(checking_p[0].pos[0] + delta_file*i, checking_p[0].pos[1] + delta_rank*i) for i in range(1, move[0]-2)]
                    #print("diag:", diagonal)
            # can opponent piece reach the diagonals to block
            for e in op:
                if [move for move in e.available_moves(self) if move in diagonal]:
                    #print("neither")
                    return False
        # otherwise, checkmate
        return True



class player:
    """Player class
    store player name, set color,
    play time elapsed, and capture pieces
    """

    def __init__(self, player_name, color):
        self.player_name = player_name
        self.color = color.lower()
        self.time_elapsed = 0
        self.captured = []


class piece:
    '''Chess piece class
    initialize piece with shorthand name, color, position

    '''
    n = [1, 2, 3, 4, 5, 6, 7]


    def __init__(self, name, color, pos):
        '''Initialze chess piece
        with short hand name, color,
        and initial position.

        '''
        self.piece_name = name
        self.color = color
        self.pos = pos
        self.moves = []

    def __str__(self):
        if self.color == 'white':
            return self.piece_name.upper()
        else:
            return self.piece_name.lower()

    def valid_move(self, file, rank, move, game, x=1):
        '''Check if the legal move of a piece
        is possibile in current board state.

        '''
        new_file = file + move[0] * x
        new_rank = rank + move[1] * x
        # Cannot be out of bound
        if new_file < 1 or new_file > 8 or new_rank < 1 or new_file > 8:
            return False
        # If the new position already had a piece,
        # it cannot be of same color, and path should
        # be cleared except for knight.
        if (new_file, new_rank) in game.board.keys():
            if game.board[(new_file, new_rank)].color == self.color:
                return False
            if self.piece_name == 'p' and new_file != file:
                return True
            elif self.piece_name in 'rbq' and self.clear_path(file, rank, move, game, x):
                return True
            elif self.piece_name in 'nk':
                return True
        # If the new position does not contain a piece,
        # the path should be cleared except for knight.
        else:
            if self.piece_name == 'p' and new_file == file and self.clear_path(file, rank, move, game, x):
                return True
            elif self.piece_name in 'rbq' and self.clear_path(file, rank, move, game, x):
                return True
            elif self.piece_name in 'nk':
                return True
        return False

    def clear_path(self, file, rank, move, game, x):
        """Check if the path
        to a new positon is clear of other pieces
        """
        for i in range(1, x):
            new_file = file + move[0] * i
            new_rank = rank + move[1] * i
            if (new_file, new_rank) in game.board:
                return False
        return True


class Pawn(piece):
    """Pawn class, child of piece
    Redefines the available moves for a pawn.
    """
    def available_moves(self, game):
        file = self.pos[0]
        rank = self.pos[1]
        unit = [(0, 1), (-1, 1), (1, 1)]
        if self.color == 'black':
            unit = [(0, -1), (-1, -1), (1, -1)]
        n = [1]
        if rank == 2 or rank == 7:
            n = [1, 2]
        avail = []
        for i in unit:
            for x in n:
                if i in [(0, 1), (0, -1)] and self.valid_move(file, rank, i, game, x):
                    avail.append((i[0]*x, i[1]*x))
                elif self.valid_move(file, rank, i, game):
                    avail.append((i[0], i[1]))
        return [(file + i[0], rank + i[1]) for i in avail]


class Rook(piece):
    """Rook class, child of piece
    Redefines the available moves for a rook.
    """
    def available_moves(self, game):
        file = self.pos[0]
        rank = self.pos[1]
        unit = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        avail = []
        for i in unit:
            for x in self.n:
                if self.valid_move(file, rank, i, game, x):
                    avail.append((i[0]*x, i[1]*x))
        return [(file + i[0], rank+ i[1]) for i in avail]


class Knight(piece):
    """Knight class, child of piece
    Redefines the available moves for a knight.
    """
    def available_moves(self, game):
        file = self.pos[0]
        rank = self.pos[1]
        unit = [(-1, 2), (1, 2), (-2, 1), (2, 1),
                (-1, -2), (1, -2), (-2, -1), (2, -1)]
        avail = []
        for i in unit:
            if self.valid_move(file, rank, i, game):
                avail.append((i[0], i[1]))
        return [(file + i[0], rank + i[1]) for i in avail]


class Bishop(piece):
    """Bishop class, child of piece
    Redefines the available moves for a bishop.
    """
    def available_moves(self, game):
        file = self.pos[0]
        rank = self.pos[1]
        unit = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        avail = []
        for i in unit:
            for x in self.n:
                if self.valid_move(file, rank, i, game, x):
                    avail.append((i[0]*x, i[1]*x))
        return [(file + i[0], rank + i[1]) for i in avail]


class Queen(piece):
    """Queen class, child of piece
    Redefines the available moves for a queen.
    """
    def available_moves(self, game):
        file = self.pos[0]
        rank = self.pos[1]
        unit = [(0, 1), (0, -1), (-1, 0), (1, 0),
                (1, 1), (-1, 1), (1, -1), (-1, -1)]
        avail = []
        for i in unit:
            for x in self.n:
                if self.valid_move(file, rank, i, game, x):
                    avail.append((i[0]*x, i[1]*x))
        return [(file + i[0], rank + i[1]) for i in avail]


class King(piece):
    """King class, child of piece
    Redefines the available moves for a king.
    """
    def available_moves(self, game):
        file = self.pos[0]
        rank = self.pos[1]
        unit = [(0, 1), (0, -1), (-1, 0), (1, 0),
                (1, 1), (-1, 1), (1, -1), (-1, -1)]
        avail = []
        for i in unit:
                if self.valid_move(file, rank, i, game):
                    avail.append((i[0], i[1]))
        return [(file + i[0], rank + i[1]) for i in avail]


interactive()
