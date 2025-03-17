class Piece:
    def __init__(self):
        self.number_of_moves = 0 



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
        # board[row][col]
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
        self.result = "" 


    def update_board(self, move: str, kingside_castle: bool, queenside_castle: bool, en_passant: bool): 
        # Update the board. 
        # capture: whether or not the move captured another piece. 

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

        return
        

    def chess_notation(self, move: str, valid: bool, piece: object, capture: bool,
                       kingside_castle: bool, queenside_castle: bool, pawn_prom: bool) -> str:
        # Format: {piece if not pawn}{starting pos}{x if capture}{ending pos}{=Q if promotion}
        # Everything should be lowercase except for '=Q' for promotion. 
        notation = ""

        if valid == False:
            # Return empty string if the move is invalid. 
            return notation
        
        elif kingside_castle == True:
            return "0-0"
        
        elif queenside_castle == True: 
            return "0-0-0"
        
        else: 
            if (piece.piece_type != 'p') or (piece.piece_type != 'P'): 
                # It is not a pawn. 
                notation = notation + piece.piece_type.lower() # check that this is proper string. 
            
            if capture == True: 
                notation = notation + move[0:2].lower() + "x" + move[2:4].lower()
            else: # Nothing was captured. 
                notation = notation + move.lower()

            if pawn_prom == True: 
                notation = notation + "=Q"
            
            return notation
        
    
    def dir_increment_decrement(start: int, end: int) -> int:
        # Function to decide if we increment or decrement from start to end. 
        if start - end > 0:
            return -1 
        else:
            return 1
        
    
    def is_same_tile(self, move: str) -> bool:
        if (move[0:2] == move[2:4]):
            return True
        else:
            return False
        

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

            direction = self.dir_increment_decrement(start_col, end_col)
            
            for i in range(start_row + direction, end_row, direction):
                if (self.board[start_row][i] != ''):
                    return False
                
        elif start_col == end_col: # Moving along a col, row changes. 

            direction = self.dir_increment_decrement(start_row, end_row)

            for i in range(start_row + direction, end_row, direction):
                if (self.board[i][start_col] != ''):
                    return False
                
        else: # Rook is moving properly. 
            return True


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
        direction_hor = self.dir_increment_decrement(start_col, end_col)
        direction_ver = self.dir_increment_decrement(start_row, end_row)

        for i,j in zip(range(start_col + direction_hor, end_col, direction_hor), 
                       range(start_row + direction_ver, end_row, direction_ver)):
            if (self.board[j][i] != ''):
                return False
            
        return True
    

    def queen_movement_valid(self, move: str) -> bool:
        # The queen's can move in any direction, as long as it's in a straight line.
        # Horizontal, vertical, and diagonal. Basically a combination of rook and bishop movements. 
        hor_or_vert = self.rook_movement(self, move) # <- CHECK THIS SYNTAX. 
        diag = self.bishop_movement(self, move)

        # Queen is moving properly if it moves either like a rook or a bishop.
        if (hor_or_vert or diag):
            return True
        else: 
            return False

    
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
    def move_pawn(self, start_tile: str, target_tile: str) -> tuple(bool, bool, bool, bool):
        pass
        # handle capturing diagonally
        # handle en passant
        # handle promotion

    def move_knight(self, start_tile: str, target_tile: str) -> bool:
        pass

    def move_bishop(self, start_tile: str, target_tile: str) -> bool:
        pass

    def move_rook(self, start_tile: str, target_tile: str) -> bool, bool:
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