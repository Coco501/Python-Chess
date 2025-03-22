class Piece:
    # initializing the piece class
    def __init__(self, piece_type, piece_color, currPos):
        self.piece_type = piece_type
        self.piece_color = piece_color
        self.currPos = currPos
        self.hasMoved = False

    def __str__(self):
        return f"{self.piece_type}"

    def __repr__(self):
        return self.__str__()


class ChessLogic:
    def __init__(self):
        """
        Initalize the ChessLogic Object. External fields are board and result

        board -> Two Dimensional List of string Representing the Current State of the Board
            P, R, N, B, Q, K - White Pieces

            p, r, n, b, q, k - Black Pieces

            '' - Empty Square

        result -> The current result of the game
            w - White Win

            b - Black Win

            d - Draw

            '' - Game In Progress
        """

        # self.board[row][col]
        self.board = [
			['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
			['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
			['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
		]

        self.boardOfPieceInstances = [
            [Piece('r', 'black', (0,0)), Piece('n', 'black', (1,0)), Piece('b', 'black', (2,0)), Piece('q', 'black', (3,0)), Piece('k', 'black', (4,0)), Piece('b', 'black', (5,0)), Piece('n', 'black', (6,0)), Piece('r', 'black', (7,0))],
            [Piece('p', 'black', (i,1)) for i in range(8)],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Piece('P', 'white', (i,6)) for i in range(8)],
            [Piece('R', 'white', (0,7)), Piece('N', 'white', (1,7)), Piece('B', 'white', (2,7)), Piece('Q', 'white', (3,7)), Piece('K', 'white', (4,7)), Piece('B', 'white', (5,7)), Piece('N', 'white', (6,7)), Piece('R', 'white', (7,7))]
        ]

        self.result = ""
        self.prev_move_played = "" # Holds the previous move.
        self.white_king_pos = "e1" # Position of both kings
        self.black_king_pos = "e8"
        self.whoseTurn: bool = True # Boolean value keeping track of whose turn it is, True = white's turn, False = black's turn


    def display_board(self):
        for row in self.board:
            print([p if p != "" else " " for p in row])

    '''
    PIECE-SPECIFIC FUNCTIONS
    '''

    ''' PAWN '''
    def pawn_movement_valid(self, move: str, piece_on_end_tile: bool) -> tuple[bool, bool, bool, bool]:
        isPawnMoveAllowed = True
        pawn_prom = False
        en_passant = False
        capture = piece_on_end_tile

        # Convert chess notation to board indices.
        start_tile = move[0:2]
        end_tile = move[2:4]
        row, col = self.chess_notation_to_indices(start_tile)
        target_row, target_col = self.chess_notation_to_indices(end_tile)

        # Checks if pawn is moving forward. Can't move backwards!
        moveForward = self.is_pawn_moving_forward(row, col, target_row)
        if (not moveForward):
            return False

        # Check if the pawn is moving forward either one or two squares.
        if col == target_col:
            # Check if the pawn is moving one square forward
            if abs(row - target_row) == 1:
                isPawnMoveAllowed = True
                pawn_prom = self.pawn_promotion(row, col, target_row, target_col)

            # If pawn is moving two steps forward, it must be its first move.
            if abs(row - target_row) == 2:
                if(self.boardOfPieceInstances[row][col].hasMoved == True):
                    isPawnMoveAllowed = False

            # For a pawn moving forward, make sure that there is nothing on the end tile or in between.
            if piece_on_end_tile or self.pieces_between_rows(row, target_row, col):
                isPawnMoveAllowed = False

        # Check if the pawn is moving diagonally. Can do so for capture.
        if abs(row - target_row) == 1 and abs(col - target_col) == 1:
                if piece_on_end_tile == True:
                    # End tile had opponent's piece.
                    # Correctly moved diagonal to capture.
                    isPawnMoveAllowed = True

                else: # End tile doesn't have a piece on it. Allowed for en passant.
                    en_passant = self.is_en_passant(move)
                    capture = True

                    if en_passant:
                        isPawnMoveAllowed = True
                    else: # Not en passant and no piece was captured.
                        isPawnMoveAllowed = False

        return isPawnMoveAllowed, capture, pawn_prom, en_passant

    ''' PAWN HELPER '''
    def is_pawn_moving_forward(self, row, col, target_row) -> bool:
        isPawnMovingForward = False

        if self.boardOfPieceInstances[row][col].piece_color == "black" and int(row) < int(target_row):
            isPawnMovingForward = True

        if self.boardOfPieceInstances[row][col].piece_color == "white" and int(row) > int(target_row):
            isPawnMovingForward = True

        else:
            isPawnMovingForward = False

        return isPawnMovingForward

    ''' ROOK '''
    def rook_movement_valid(self, move: str) -> bool:
        start_tile = move[0:2]
        end_tile = move[2:4]

        start_row, start_col = self.chess_notation_to_indices(start_tile)
        end_row, end_col = self.chess_notation_to_indices(end_tile)

        # Check that the rook is moving only horizontally or vertically.
        # Either the start and end file must be the same or the start and end rank must be the same, but
        # can't both be true.
        # There is already another function to check that it is not staying in the same tile.
        if (start_row != end_row) and (start_col != end_col):
            return False

        # Check that the rook is not jumping over any pieces.
        # Doesn't check if it has captured a piece.
        if start_row == end_row: # Moving along a row, col changes. Board[var][const]. Board[rank][file]. Board[row][col].
            if self.pieces_between_cols(start_col, end_col, start_row):
                return False

        elif start_col == end_col: # Moving along a col, row changes.
            if self.pieces_between_rows(start_row, end_row, start_col):
                return False

        else: # Rook is moving properly.
            return True

        return False

    ''' KNIGHT '''
    def knight_movement_valid(self, move: str) -> bool:
        isKnightMoveAllowed = True
        start_tile = move[0:2]
        target_tile = move[2:4]

        row, col = self.chess_notation_to_indices(start_tile)
        target_row, target_col = self.chess_notation_to_indices(target_tile)

        # check for proper movement
        if abs(row - target_row) == 2 and abs(col - target_col) == 1:
            isKnightMoveAllowed = True

        elif abs(row - target_row) == 1 and abs(col - target_col) == 2:
            isKnightMoveAllowed = True

        else:
            isKnightMoveAllowed = False

        return isKnightMoveAllowed

    ''' BISHOP '''
    def bishop_movement_valid(self, move: str) -> bool:
        start_tile = move[0:2]
        end_tile = move[2:4]

        start_row, start_col = self.chess_notation_to_indices(start_tile)
        end_row, end_col = self.chess_notation_to_indices(end_tile)

        # Check that the bishop moved only diagonally. The distance moved horizontally should be
        # the same as the distance moved vertically.
        dist_hor = abs(start_row - end_row)
        dist_ver = abs(start_col - end_col)

        if (dist_hor != dist_ver): # Bishop not moving diagonally properly.
            return False

        # Check that the bishop is not jumping over any pieces.
        if self.pieces_along_diagonal(start_row, end_row, start_col, end_col):
            return False

        return True

    ''' YASS QUEEN '''
    def queen_movement_valid(self, move: str) -> bool:
        # The queen's can move in any direction, as long as it's in a straight line.
        # Horizontal, vertical, and diagonal. Basically a combination of rook and bishop movements.
        hor_or_vert = self.rook_movement_valid(move)
        diag = self.bishop_movement_valid(move)

        # Queen is moving properly if it moves either like a rook or a bishop.
        return hor_or_vert or diag

    ''' KING '''
    def king_movement_valid(self, move: str) -> tuple[bool, bool, bool]:
        valid = True
        kingside_castle = False
        queenside_castle = False

        # Get indices.
        start_tile = move[0:2]
        end_tile = move[2:4]

        start_row, start_col = self.chess_notation_to_indices(start_tile)
        end_row, end_col = self.chess_notation_to_indices(end_tile)

        # Check if King is moving only one square in any direction.
        change_in_rows = abs(start_row - end_row)
        change_in_cols = abs(start_col - end_col)

        if (change_in_rows <= 0 and change_in_cols <= 0):
            # The King has only moved one square, so no possibility of a castle.
            # This is a valid way for the king to move.
            valid = True
            kingside_castle = False
            queenside_castle = False

        elif (change_in_rows == 0 and change_in_cols == 2):
            # There is potentially a castle.
            valid, kingside_castle, queenside_castle = self.is_valid_castle(start_row, start_col, end_row, end_col)

        else:
            valid = False
            kingside_castle = False
            queenside_castle = False

        return valid, kingside_castle, queenside_castle



    '''
    EDGE CASES
    '''

    ''' PAWN PROMOTION '''
    def pawn_promotion(self, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        if self.board[start_row][start_col] == 'P': # White pawn.
            if end_row == 0:
                return True
            else:
                return False

        else: # Black pawn
            if end_row == 7:
                return True
            else:
                return False

    ''' EN PASSANT '''
    def is_en_passant(self, move: str) -> bool:
        # Get indices of current move.
        start_row, start_col = self.chess_notation_to_indices(move[0:2])
        end_row, end_col = self.chess_notation_to_indices(move[2:4])

        # Get indices of previous move.
        prev_start_row, prev_start_col = self.chess_notation_to_indices(self.prev_move_played[0:2])
        prev_end_row, prev_end_col = self.chess_notation_to_indices(self.prev_move_played[2:4])

        # Check that the previous move was a pawn.
        piece = self.board[prev_end_row][prev_end_col]
        if piece.lower() != 'p':
            return False

        # Find direction our pawn is moving in terms of rows. Is it moving up or down rows?
        direction = self.dir_increment_decrement(start_row, end_row)

        # Check that in the previous move, opponent's pawn moved forward into the right position.
        # The previous start and end columns should be the same as the current end column.
        if prev_start_col == prev_end_col == end_col:
            if start_row == prev_end_row:
                if prev_start_row == end_row + direction:
                    return True

        return False

    ''' CASTLING '''
    def is_valid_castle(self, start_row: int, start_col: int, end_row: int, end_col: int) -> tuple[bool, bool, bool]:
        valid = False
        kingside_castle = False
        queenside_castle = False

        # Check that the king has not previously moved.
        king = self.boardOfPieceInstances[start_row][start_col]
        if king.hasMoved == True:
            return valid, kingside_castle, queenside_castle

        # Check that the rook involved has not previously moved.
        if (end_col - start_col > 0): # Possible kingside castle.
            rook = self.boardOfPieceInstances[end_row][7]
        else: # Possible queenside castle.
            rook = self.boardOfPieceInstances[end_row][0]

        if rook.hasMoved == True:
            return valid, kingside_castle, queenside_castle

        # Check that there are no pieces between the king and the rook.
        # Check kingside:
        if (end_col - start_col > 0):
            if self.pieces_between_cols(start_col, 7, start_row):
                return valid, kingside_castle, queenside_castle
            kingside_castle = True

        else: # Check queenside.
            if self.pieces_between_cols(start_col, 0, start_row):
                return valid, kingside_castle, queenside_castle
            queenside_castle = True

        # TODO: Check that the king is not passing through or land on a square that is under attack.
        #
        #

        return valid, kingside_castle, queenside_castle


    def player_in_check(self, move: str) -> bool:

        # TODO:
        # From king's position, try combinatations of ways pieces can move.
            # Start at king, and increment outwards.
                # Check along the vertical until we hit a piece.
                    # If we do, check if that piece is an opponent's piece.
                    # Check if that piece is a rook or queen, something that can move in that way.
                        # If true, then the king is in check.
                # Check along the horizontal until we hit a piece.
                    # If we do, check if that piece is an opponent's piece.
                        # Check if that piece is a rook or queen, something that can move in that way.
                            # If true, then the king is in check.


        # TODO:
        # From king's position, try combinatations of ways pieces can move.

        kings_rank, kings_file = self.chess_notation_to_indices(move)

        # TODO:
        # From king's position, try combinatations of ways pieces can move.

        # Check the rank
        rank_found_piece = False
        for test_file in range(0, 8):
            piece = self.board[kings_rank][test_file]

            # The pieces that can move up and down the whole board
            # TODO: Check the other color's pieces, not the lower case ones
            if piece in ["q", "r"]:
                return True

        # Check the file
        file_found_piece = False
        for test_rank in range(0, 8):
            piece = self.board[test_rank][kings_file]

            # TODO: Check the other color's pieces, not the lower case ones
            if piece in ["q", "r"]:
                return True

            # Start at king, and increment outwards.
                # Check along the vertical until we hit a piece.
                    # If we do, check if that piece is an opponent's piece.
                    # Check if that piece is a rook or queen, something that can move in that way.
                        # If true, then the king is in check.
                # Check along the horizontal until we hit a piece.
                    # If we do, check if that piece is an opponent's piece.
                        # Check if that piece is a rook or queen, something that can move in that way.
                            # If true, then the king is in check.

                # Check along diagonals.
                    # Check for queen, bishop, rook.
                # Check the spaces that a knight can be.
                    # Change in 2 along one axis, change in 1 along the other axis.


        # TODO: We'll need a way to keep track of where the king is.
            # Probably just add another class variable.

        # Also we need to check both kings, because current player can't leave their king in check,
        # and we also have to check if they've put the opponent in check.

        return False

    ''' CHECKMATE '''
    def player_in_checkmate(self) -> bool:
        # TODO:
        # Call check from all of the possible spaces a king can move to? 8 spaces.

        # Move the king to any place available in one move
        # Then check to see if the king is in check for all spaces
        # Try to move pieces to block check from happening

        is_player_white = True

        j = 0
        i = 0
        for i, row in enumerate(self.board):
            if is_player_white:
                j = row.index("K")
            else:
                j = row.index("k")

        king_pos = self.index_to_move(i, j)

        # Check everywhere around the king
        self.player_in_check(king_pos)

        return False

    ''' STALEMATE '''
    def stalemate(self) -> bool:
        # If player is not in check, but there is no move the player can make without putting their king in check.

        return False


    '''
    HELPER FUNCTIONS
    '''

    def chess_notation_to_indices(self, tile: str) -> tuple[int, int]:
        file = tile[0]  # 'a'-'h'
        rank = tile[1]  # '1'-'8'

        col = ord(file) - ord('a')  # 0-7
        row = 8 - int(rank)         # 0-7 (rank 1 = row 7)

        return row, col


    def index_to_move(self, row: int, col: int):
        c = chr(col + ord("a"))
        r = abs(row - 8)
        return f"{c}{r}"


    def own_piece_at_tile(self, tile: str) -> bool:
        # potential error, using isupper() or islower() on empty string '' or ' ' could raise error?
        row, col = self.chess_notation_to_indices(tile)

        if self.whoseTurn == True:  # white's turn
            if self.board[row][col].isupper():
                return True

        elif self.whoseTurn == False:  # black's turn
            if self.board[row][col].islower():
                return True

        return False  # default


    def opponent_piece_at_tile(self, tile: str) -> bool:
        row, col = self.chess_notation_to_indices(tile)

        if self.whoseTurn == True:  # white's turn
            if self.board[row][col].islower():
                return True

        elif self.whoseTurn == False:  # black's turn
            if self.board[row][col].isupper():
                return True

        return False # default


    def dir_increment_decrement(self, start: int, end: int) -> int:
        # Function to decide if we increment or decrement from start to end.
        if start - end > 0:
            return -1
        else:
            return 1


    def is_same_tile(self, move: str) -> bool:
        return move[0:2] == move[2:4] # returns true if a move from one tile to itself


    def pieces_between_cols(self, start_col: int, end_col: int, row: int) -> bool:
        # Checks if there are any pieces in between two tiles. Col changes, row stays const.
        direction = self.dir_increment_decrement(start_col, end_col)

        for i in range(start_col + direction, end_col, direction):
             if (self.board[row][i] != ''):
                return True

        return False


    def pieces_between_rows(self, start_row: int, end_row: int, col: int) -> bool:
        # Checks if there are any pieces in between two tiles. Row changes, col stays const.
        direction = self.dir_increment_decrement(start_row, end_row)

        for i in range(start_row + direction, end_row, direction):
            if (self.board[i][col] != ''):
                return True

        return False


    def pieces_along_diagonal(self, start_row: int, end_row: int, start_col: int, end_col: int) -> bool:
        # Checks if there are any pieces in between two tiles along a diagonal.
        direction_hor = self.dir_increment_decrement(start_col, end_col)
        direction_ver = self.dir_increment_decrement(start_row, end_row)

        for i,j in zip(range(start_col + direction_hor, end_col, direction_hor),
                       range(start_row + direction_ver, end_row, direction_ver)):
            if (self.board[j][i] != ''):
                return True


    def update_king_position(self, square: str):
        row, col = self.chess_notation_to_indices(square)

        # Check if king moved.
        if self.board[row][col].lower() == 'k':

            if self.whoseTurn == True: # White's turn
                self.white_king_pos = square

            else: # Black's turn
                self.black_king_pos = square

    '''
    PRINCIPAL FUNCTIONS CALLED BY MAIN
    '''

    def update_piece_and_boardOfPieceInstances(self, move: str, kingside_castle: bool, queenside_castle: bool, en_passant: bool):
        start_tile = move[0:2]
        end_tile = move[2:4]

        start_row, start_col = self.chess_notation_to_indices(start_tile)
        end_row, end_col = self.chess_notation_to_indices(end_tile)

        # Update the board of piece instances.
        self.boardOfPieceInstances[end_row][end_col] = self.boardOfPieceInstances[start_row][start_col]
        self.boardOfPieceInstances[start_row][start_col] = None

        if kingside_castle == True:
            # King as already moved.
            # Move the rook.
            self.boardOfPieceInstances[end_row][end_col - 1] = self.boardOfPieceInstances[start_row][start_col + 3]
            self.boardOfPieceInstances[start_row][start_col + 3] = None

        if queenside_castle == True:
            # King as already moved.
            # Move the rook.
            self.boardOfPieceInstances[end_row][end_col + 1] = self.boardOfPieceInstances[start_row][start_col - 4]
            self.boardOfPieceInstances[start_row][start_col - 4] = None

        if en_passant == True:
            # The pawn has been moved.
            # Must remove the captured pawn from the board.
            self.boardOfPieceInstances[start_row][end_col] = ''

        # Update the piece instance.
        self.boardOfPieceInstances[end_row][end_col].currPos = (end_col, end_row) # ASK JASH ABOUT THE CURRPOS.
        self.boardOfPieceInstances[end_row][end_col].hasMoved = True


    def update_board(self, move: str, kingside_castle: bool, queenside_castle: bool, en_passant: bool, pawn_prom: bool):
        # Update the board.

        start_tile = move[0:2]
        end_tile = move[2:4]

        start_row, start_col = self.chess_notation_to_indices(start_tile)
        end_row, end_col = self.chess_notation_to_indices(end_tile)

        # Move the piece.
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = ''

        if kingside_castle == True:
            # King as already moved.
            # Move the rook.
            self.board[end_row][end_col - 1] = self.board[start_row][start_col + 3]
            self.board[start_row][start_col + 3] = ''

        if queenside_castle == True:
            # King as already moved.
            # Move the rook.
            self.board[end_row][end_col + 1] = self.board[start_row][start_col - 4]
            self.board[start_row][start_col - 4] = ''

        if en_passant == True:
            # The pawn has been moved.
            # Must remove the captured pawn from the board.
            self.board[start_row][end_col] = ''

        if pawn_prom == True:
            # Replace the pawn with a queen.
            if self.whoseTurn == True: # White's turn.
                self.board[end_row][end_col] = 'Q'
            else: # Black's turn
                self.board[end_row][end_col] = 'q'


    ''' Converts a valid move into chess notation '''
    def chess_notation(self, move: str, valid: bool, capture: bool, kingside_castle: bool,
                       queenside_castle: bool, pawn_prom: bool) -> str:
        # Format: {piece if not pawn}{starting pos}{x if capture}{ending pos}{=Q if promotion}
        # Everything should be lowercase except for '=Q' for promotion.

        start_row, start_col = self.chess_notation_to_indices(move[0:2])
        piece = self.board[start_row][start_col]

        notation = ""

        if valid == False:
            # Return empty string if the move is invalid.
            return notation

        elif kingside_castle == True:
            return "0-0"

        elif queenside_castle == True:
            return "0-0-0"

        else:
            if (piece.lower() != 'p'):
                # It is not a pawn.
                notation = notation + piece.lower() # check that this is proper string.

            if capture == True:
                notation = notation + move[0:2].lower() + "x" + move[2:4].lower()
            else: # Nothing was captured.
                notation = notation + move.lower()

            if pawn_prom == True:
                notation = notation + "=Q"

            return notation


    def is_valid_move(self, move: str):
        valid = True
        capture = False
        kingside_castle = False
        queenside_castle = False
        pawn_prom = False
        en_passant = False
        game_over = False
        draw = False

        start_row, start_col = self.chess_notation_to_indices(move[0:2])
        end_row, end_col = self.chess_notation_to_indices(move[2:4])

        piece = self.board[start_row][start_col].lower()

        # Checking general valid/invalid, not specific to piece type.
        # Start and end tile should not be the same, starting tile should have own piece,
        # ending tile should not have own piece.
        # The own_piece_at_tile function should take care of checking that the starting tile is not empty.
        valid = ((not self.is_same_tile(move)) and (self.own_piece_at_tile(move[0:2]))
                 and (not self.own_piece_at_tile(move[2:4])))

        if valid:
            # Check if piece was captured at end tile, and that it was the opponent's piece.
            # This doesn't cover the en passant edge case.                                      <- MAKE SURE TO COVER THIS IN EN PASSANT.
            capture = self.opponent_piece_at_tile(move[2:4])

            # Checking piece specific valid/invalid.
            if piece == 'p': # pawn
                valid, capture, pawn_prom, en_passant = self.pawn_movement_valid(move, capture)

            elif piece == 'r': # rook
                valid = self.rook_movement_valid(move)

            elif piece == 'n': # knight
                valid = self.knight_movement_valid(move) # check

            elif piece == 'b': # bishop
                valid = self.bishop_movement_valid(move)

            elif piece == 'q': # queen
                valid = self.queen_movement_valid(move)

            elif piece == 'k': # king
                valid, kingside_castle, queenside_castle = self.king_movement_valid()

            # Check for checks, checkmates, stalemates.
            white_win, black_win, draw = self.is_game_over()
            # TODO DO WE NEED TO ONLY CHECK FOR CHECK IF THERE WAS A VALID MOVE PLAYED?


        return valid, capture, kingside_castle, queenside_castle, pawn_prom, en_passant, white_win, black_win, draw


    def player_in_future_check(self, king_pos: str):
        # check surrounding 8 squares of king, if all surrounding squares would be in check, return true
        # convert king_pos to board indices
        row, col = self.chess_notation_to_indices(king_pos)
        king: str = self.board[row][col] 
        lastpiece: str

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),            (0, 1),
            (1, -1), (1, 0), (1,1)
        ]

        for rd, cd in directions:
            if (row == 0 and rd == -1) or (row == 7 and rd == 1) or (col == 0 and cd == -1) or (col == 7 and cd == 1):
                continue # skip due to out of bounds

            new_row, new_col = row + rd, col + cd
            chessnotation = self.index_to_move(new_row, new_col)
            lastpiece = self.board[new_row][new_col]
            if not ((lastpiece.islower() and king.islower) or (lastpiece.isupper() and king.isupper())): # not moving onto own piece
                self.board[new_row][new_col] = king # temporarily move king
                self.board[row][col] = '' # king moved away
                if not self.player_in_check(chessnotation): # TODO: ARGUMENTS EXPECTING CHESS NOTATION, change signature?
                    # restore board
                    self.board[row][col] = king
                    self.board[new_row][new_col] = lastpiece
                    return False # king not in check when moved
                

    def is_game_over(self) -> tuple[bool, bool, bool]:
        check_player = False
        check_opponent = False
        future_check_player = False # If any of the king's escape routes will end in check.
        future_check_opponent = False
        stalemate = False
        black_win = False
        white_win = False

        # 1) Check that move does not leave own king in check.
        # 2) And check whether move places opponent's king in check.
        # 3) Check for possible Checkmate. Check if king will be in check if it tries to escape
        # to surrounding pieces.
        if self.whoseTurn == True: # White's turn.
            if self.player_in_check(self.white_king_pos):
                check_player = True
            if self.player_in_check(self.black_king_pos):
                check_opponent = True

            if self.player_in_future_check(self.white_king_pos):
                future_check_player = True
            if self.player_in_future_check(self.black_king_pos):
                future_check_opponent = True

            # Checkmate conditions:
            if check_player and future_check_player:
                # White is in checkmate.
                black_win = True
            if check_opponent and future_check_opponent:
                white_win = True

        else: # Black's turn.
            if self.player_in_check(self.black_king_pos):
                check_player = True
            if self.player_in_check(self.white_king_pos):
                check_opponent = True

            if self.player_in_future_check(self.black_king_pos):
                future_check_player = True
            if self.player_in_future_check(self.white_king_pos):
                future_check_opponent = True

            # Checkmate conditions:
            if check_player and future_check_player:
                # Black is in checkmate.
                white_win = True
            if check_opponent and future_check_opponent:
                black_win = True


        # TODO # Stalemate conditions.
        # if (not check_player) and future_check:
        #     # TODO: Check for Stalemate.
        #     pass

        return white_win, black_win, stalemate


    # ----------------------------------------------------------------- #
    # Main Function --------------------------------------------------- #

    def play_move(self, move: str) -> str:
        """
        Function to make a move if it is a valid move. This function is called everytime a move is made on the board

        Args:
            move (str): The move which is proposed. The format is the following: starting_square}{ending_square}

            i.e. e2e4 - This means that whatever piece is on E2 is moved to E4

        Returns:
            str: Extended Chess Notation for the move, if valid. Empty str if the move is invalid
        """

        # Initialize Booleans.
        valid = True            # Is the move valid?
        capture = False         # Did we capture another piece?
        kingside_castle = False
        queenside_castle = False
        pawn_prom = False
        en_passant = False
        draw = False

        # parse_move() # Already done in the other functions.

        # Check if move is valid.
        valid, capture, kingside_castle, queenside_castle, pawn_prom, en_passant, white_win, black_win, draw = self.is_valid_move(move)

        # Write out the extended chess notation.
        notation = self.chess_notation(move, valid, capture, kingside_castle, queenside_castle, pawn_prom)

        # If the move is valid, update the board and results.
        if valid:
            self.update_board(move, kingside_castle, queenside_castle, en_passant, pawn_prom) # Update the board.
            self.update_piece_and_boardOfPieceInstances(move, kingside_castle, queenside_castle, en_passant) # TODO ADD PAWN PROMOTION.

            # Update the previous move to move that was just played.
            self.prev_move_played = move

            # Update the king position if king was just moved.
            self.update_king_position(move[2:4])

            # Update which player's turn it is.
            self.whoseTurn = not self.whoseTurn

            # Update the 'result' field.
            if draw:
                self.result = "d"
            elif white_win:
                self.result = "w"
            elif black_win:
                self.result = "b"

            # Else, the game hasn't ended yet, so the result is still empty.

        return notation

# FOR TESTING?
"""
# creates an instance of ChessLogic
gameLogic = ChessLogic()

# jash testing purposes?
print("e2 to e4:", gameLogic.pawn_movement_valid("e2", "e4"))  # Valid: White pawn moves two squares forward from start
print("d7 to d5:", gameLogic.pawn_movement_valid("d7", "d5"))
print("e4 to d5:", gameLogic.pawn_movement_valid("e4", "d5"))  # Valid: White pawn captures black pawn
"""
