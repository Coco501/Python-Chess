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
		
		# boolean value keeping track of whose turn it is, true = white's turn, false = black's turn
        self.whoseTurn: bool = True

    def play_move(self, move: str) -> str:
        """
        Function to make a move if it is a valid move. This function is called everytime a move in made on the board

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
    def move_pawn(self, start_tile: str, target_tile: str) -> tuple[bool, bool, bool, bool]:
        pass
        # handle capturing diagonally
        # handle en passant
        # handle promotion

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

    def chess_notation_to_indices(self, tile: str) -> tuple[int, int]:
        file = tile[0]  # 'a'-'h'
        rank = tile[1]  # '1'-'8'

        col = ord(file) - ord('a')  # 0-7
        row = 8 - int(rank)         # 0-7 (rank 1 = row 7)

        return row, col

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