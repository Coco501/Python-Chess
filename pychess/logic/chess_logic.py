class Piece: 
    # initializing the piece class
    def __init__(self, piece_type, piece_color, currPos):
        self.piece_type = piece_type
        self.piece_color = piece_color
        self.currPos = currPos
        self.numMoves = numMoves = 0
        self.hasMoved = hasMoved = False

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
        # 
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
     
        pass
        
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

print("e2 to e4:", gameLogic.move_pawn("e2", "e4"))  # Valid: White pawn moves two squares forward from start
print("d7 to d5:", gameLogic.move_pawn("d7", "d5"))
print("e4 to d5:", gameLogic.move_pawn("e4", "d5"))  # Valid: White pawn captures black pawn