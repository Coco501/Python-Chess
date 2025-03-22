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

    
    def is_valid_move(self, move: str): # FINISH THIS HERE. 
        valid = True 
        capture = False 
        kingside_castle = False 
        queenside_castle = False
        pawn_prom = False
        en_passant = False
        game_over = False
        ## Need a var or bool for winner or draw? 

        # Checking general valid/invalid, not specific to piece type. 
        # Start and end tile should not be the same, starting tile should have own piece, 
        # ending tile should not have own piece. 
        valid = ((not self.is_same_tile(self, move)) and (self.own_piece_at_tile(self, move[0:2])) 
                 and (not self.own_piece_at_tile(self, move[2:4])))
        
        if valid:
            # Check if piece was captured at end tile, and that it was the opponent's piece. 
            capture = self.opponent_piece_at_tile(self, move[2:4])

            # piece =  # FINISH THIS HERE

            # Checking piece specific valid/invalid. 
            match piece: # <- MIGHT HAVE TO END UP USING IF STATEMENTS INSTEAD. 
                case 'p': # Pawn 
                    valid = self.is_valid_pawn()

                    if valid:
                        pawn_prom = self.is_pawn_prom()
                        en_passant = self.is_en_passant()

                case 'n': # knight
                    valid = self.knight_movement_valid() # check
                
                case 'b': # bishop
                    valid = self.bishop_movement_valid(self, move)
                
                case 'r': # rook
                    valid = self.rook_movement_valid(self, move)
                
                case 'q': # queen
                    valid = self.queen_movement_valid(self, move)
                
                case 'k': # king
                    valid = self.king_movement_valid()

                    if valid:
                        kingside_castle = self.is_kingside_castle()
                        queenside_castle = self.is_queenside_castle()

            # Check that move does not leave own king in check. 
            #####

            # Check whether move places opponent's king in check. 
            #####

            # Check whether move places opponent's king in checkmate. 
            #####

        return valid, capture, kingside_castle, queenside_castle, pawn_prom, en_passant, game_over


    def play_move(self, move: str) -> str:
        # Initialize Booleans. 
        valid = True            # Is the move valid? 
        capture = False         # Did we capture another piece? 
        kingside_castle = False 
        queenside_castle = False
        pawn_prom = False
        en_passant = False
        game_over = False      # Game is over when one side wins or there is a draw. 

        # parse_move() # Already done in the other functions. 

        valid, capture, kingside_castle, queenside_castle, pawn_prom, en_passant, game_over = self.is_valid_move(self, move) 

        notation = self.chess_notation(self, move, valid, piece, capture, kingside_castle, queenside_castle, pawn_prom)

        if valid: 
            self.update_board(self, move, kingside_castle, queenside_castle, en_passant) # Update the board. 

        # ADD CODE HERE TO UPDATE THE RESULT FIELD. 
        if game_over:
            pass

        return notation


        """
        Function to make a move if it is a valid move. This function is called everytime a move is made on the board

        Args:
            move (str): The move which is proposed. The format is the following: starting_square}{ending_square}

            i.e. e2e4 - This means that whatever piece is on E2 is moved to E4

        Returns:
            str: Extended Chess Notation for the move, if valid. Empty str if the move is invalid
        """

        #Implement this
        # parse starting tile and destination tile into two variables
        # figure out if there is a piece on starting tile, if not, invalid move
        #   if piece is not current user's piece, invalid move (keep track of turns)
        # append piece letter to result string (no letter for pawn)
        # call respective function for that piece
        # if valid, check if destination already has a piece
        #   if opponent piece, capture (append x to denote capture in extended chess notation)
        #   if own piece, invalid move
        # check if moving put user into check, if it did, invalid move
        # check if opponent is now in checkmate, if they are, change game state to win
        # increment number of moves for piece
        # update board state
        # change to other players turn
        pass

        '''
        pseudocode:
            ...
            str start_tile = move. first two letters
            str target_tile = move. # last two letters

            # get piece on start_tile
            piece = self.board[start_tile]
            # convert piece to lowercase so we can handle both white and black pieces
            piece = tolower(piece)

            switch(piece)
                case 'p': # pawn
                    if !move_pawn(self, start_tile, target_tile)
                        return '' # invalid move

                case 'n': # knight
                    if !move_knight(self, start_tile, target_tile)
                        return ''

                case 'b': # bishop
                    if !move_bishop(self, start_tile, target_tile)
                        return ''

                case 'r': # rook
                    if !move_rook(self, start_tile, target_tile)
                        return ''

                case 'q': # queen
                    if !move_queen(self, start_tile, target_tile)
                        return ''

                case 'k': # king
                    if !move_king(self, start_tile, target_tile)
                        return ''

                default:
                    return ''

            if moved_to_check()
                return ''   # player moved into check
        '''


    # each move function returns true if the move is possible (only considering tiles)
    # do not consider external factors like other pieces
    # some functions return tuples of bools, for special cases like en passant, promotion, castling, etc.
    def move_pawn(self, start_tile: str, target_tile: str) -> tuple[bool, bool, bool, bool]:
        isPawnMoveAllowed = True

        #'e2' on board is board[6][4]
        #'e4' on board is board[4][4]

        # check if the starting tile is a pawn
        
        # Convert chess notation to board indices correctly
        file = start_tile[0]  # 'a'-'h'
        rank = start_tile[1]  # '1'-'8'

        col = ord(file) - ord('a')  # 0-7
        row = 8 - int(rank)         # 0-7 (rank 1 = row 7)

        target_file = target_tile[0]  # 'a'-'h'
        target_rank = target_tile[1]  # '1'-'8'

        target_col = ord(target_file) - ord('a')  # 0-7
        target_row = 8 - int(target_rank)         # 0-7 (rank 1 = row 7)

        moveForward = self.make_sure_piece_is_moving_forward(row, col, target_row)

        if self.board[row][col] not in ('P', 'p'):
            print("Not a pawn... invalid move")
            isPawnMoveAllowed = False
            return (isPawnMoveAllowed, False, False, False)
            # return False

        # make sure the target tile doesn't already have a piece of the same color
        if self.board[target_row][target_col] != '': 
            if self.boardOfPieceInstances[target_row][target_col].piece_color == self.boardOfPieceInstances[row][col].piece_color:
                isPawnMoveAllowed = False

        # check if the pawn is moving forward properly
        if col == target_col:
            # check if the pawn is moving two squares forward
            if abs(row - target_row) == 2:
                # determine if this is allowed
                if(self.boardOfPieceInstances[row][col].hasMoved == True):
                    print("Can't move forward two squares after the first move")
                    isPawnMoveAllowed = False
                    
                             
                
            # check if the pawn is moving one square forward
            if abs(row - target_row) == 1:
                if moveForward == False:
                    isPawnMoveAllowed = False
                else:
                    isPawnMoveAllowed = True
                
        # could be a capture
        if abs(col - target_col) == 1:
            if moveForward == False:
                isPawnMoveAllowed = False

            # check if the pawn is moving diagonally
            if abs(row - target_row) == 1:
                # determine if this is allowed
                if self.board[target_row][target_col] == '':
                    print("No piece to capture")
                    isPawnMoveAllowed = False
                else:
                    isPawnMoveAllowed = True
                
                     
        # Handle moving logic after determining that the move is valid    
        if (isPawnMoveAllowed == True):
            # make the move

            # update the main board
            self.board[target_row][target_col] = self.board[row][col]
            self.board[row][col] = ''

            # update the board of piece instances
            self.boardOfPieceInstances[target_row][target_col] = self.boardOfPieceInstances[row][col]
            self.boardOfPieceInstances[row][col] = None

            # update the piece instance
            self.boardOfPieceInstances[target_row][target_col].currPos = (target_col, target_row)
            self.boardOfPieceInstances[target_row][target_col].numMoves += 1
            self.boardOfPieceInstances[target_row][target_col].hasMoved = True

            # print the board
            #for row in self.board:
            #   print(row)
            #print()



        return (isPawnMoveAllowed, False, False, False)

        # return False

        
    def make_sure_piece_is_moving_forward(self, row, col, target_row) -> bool:
        if self.boardOfPieceInstances[row][col].piece_color == "black" and int(row) < int(target_row):
            isPawnMovingForward = False
        if self.boardOfPieceInstances[row][col].piece_color == "white" and int(row) > int(target_row):
            isPawnMovingForward = False
        else:
            isPawnMovingForward = True

        return isPawnMovingForward

        pass
    
    def move_knight(self, start_tile: str, target_tile: str) -> bool:
    
        pass

    def move_bishop(self, start_tile: str, target_tile: str) -> bool:
        pass

    def move_rook(self, start_tile: str, target_tile: str) -> tuple[bool, bool]:
        pass
        # call castling if inputs match castling tiles
        #   handle going through check while castling (king can not move into check while castling)

    def move_queen(self, start_tile: str, target_tile: str) -> bool:
        pass

    def move_king(self, start_tile: str, target_tile: str) -> bool:
        pass

    def move_castling(self, start_tile: str, target_tile: str) -> bool:
        pass

    def moved_to_check():
        pass


# creates an instance of ChessLogic
gameLogic = ChessLogic()

# jash testing purposes?
print("e2 to e4:", gameLogic.move_pawn("e2", "e4"))  # Valid: White pawn moves two squares forward from start
print("d7 to d5:", gameLogic.move_pawn("d7", "d5"))
print("e4 to d5:", gameLogic.move_pawn("e4", "d5"))  # Valid: White pawn captures black pawn

    def chess_notation_to_indices(self, tile: str) -> tuple[int, int]:
        file = tile[0]  # 'a'-'h'
        rank = tile[1]  # '1'-'8'

        col = ord(file) - ord('a')  # 0-7
        row = 8 - int(rank)         # 0-7 (rank 1 = row 7)

        return (row, col)


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

